from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter


from .models import Game
from .schema_extensions import get_games_api_schema, post_games_api_schema, get_game_api_schema
from .serializers import GetGameSerializer, CreateGameSerializer, DummyAuthApiRequestSerializer, DummyResponseSerializer
from utils.utils import match_authenticated_user

class GamePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25

class GamesApi(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**get_games_api_schema)
    def get(self, request):
        try:
            is_authenticated, user = match_authenticated_user(request)
            if is_authenticated:
                games = Game.objects.all()

                if request.data:
                    params = request.query_params
                    if params:
                        if (genre := params.get('genre')) is not None and (year := params.get('year_released')) is not None:
                            games = Game.objects.all().filter(genre=genre, year_released=year)
                        elif (genre := params.get('genre')) is not None:
                            games = Game.objects.all().filter(genre=genre)
                        elif (year := params.get('year_released')) is not None:
                            games = Game.objects.all().filter(year_released=year)

                paginator = GamePagination()
                result_page = paginator.paginate_queryset(games, request)
                serializer = GetGameSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except MultiValueDictKeyError as e:
            message = 'Missing value for ' + e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(**post_games_api_schema)
    def post(self, request):
        try:
            is_authenticated, user = match_authenticated_user(request)
            if is_authenticated:
                request_data = request.data
                serializer = CreateGameSerializer(data=request_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'message': 'wrong input data'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'user not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except (MultiValueDictKeyError, ValueError) as e:
            message = 'Missing value for ' + e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

class GameApi(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**get_game_api_schema)
    def get(self, request, id):
        if match_authenticated_user(request):
            try:
                game = Game.objects.get(pk=id)
                serializer = GetGameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Game.DoesNotExist:
                return Response({'message': f'game with the id {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
