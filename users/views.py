from django.contrib.auth.hashers import check_password
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from .models import User, Favorites
from .serializers import CreateFavoriteSerializer, GetFavoritesSerializer, DummyAuthApiRequestSerializer, DummyResponseSerializer, DummyAuthRegisterRequestSerializer
from games.models import Game
from utils.utils import match_authenticated_user

class AuthApi(APIView):

    @extend_schema(
        request=DummyAuthApiRequestSerializer,
        responses={
            200: DummyResponseSerializer,
            400: DummyResponseSerializer,
            401: DummyResponseSerializer,
            404: DummyResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='Successful login',
                value={'message': 'Token token'},
                response_only=True,
                media_type='application/json',
                status_codes=['200']
            ),
            OpenApiExample(
                name='Login failed, credentials not valid',
                value={'message': 'credentials not valid.'},
                response_only=True,
                media_type='application/json',
                status_codes=['401']
            ),
            OpenApiExample(
                name='Login failed, missing request fields',
                value={'message': 'missing value for username'},
                response_only=True,
                media_type='application/json',
                status_codes=['400']
            ),
            OpenApiExample(
                name='Login failed, user not found',
                value={'message': 'User not found.'},
                response_only=True,
                media_type='application/json',
                status_codes=['404']
            )
        ],
        summary="Log in registered user"
    )
    def post(self, request):
        try:
            if request.data:
                user = User.objects.get(username=request.data['username'])
            else:
                return Response({'message': 'missing POST data'}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(request.data['password'], user.password):
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                return Response({'message': f'Token {token.key}'})
            else:
                return Response({'message': 'credentials not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except MultiValueDictKeyError as e:
            message = 'missing value for ' + e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

class AuthApiRegistration(APIView):

    @extend_schema(
        request=DummyAuthRegisterRequestSerializer,
        responses={
            200: DummyResponseSerializer,
            400: DummyResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='Register user',
                value={'message': 'user created'},
                response_only=True,
                media_type='application/json',
                status_codes=['200']
            ),
            OpenApiExample(
                name='Registration failed',
                value={'message': 'missing POST data'},
                response_only=True,
                media_type='application/json',
                status_codes=['401']
            )
        ],
        summary="Register a new user",
    )
    def post(self, request):
        try:
            if request.data:
                data = request.data
                User.objects.create_user(username=data['username'], password=data['password'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
                return Response({'message': 'user created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'missing POST data'}, status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError as e:
            message = 'missing value for ' + e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

class FavoritesApi(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=GetFavoritesSerializer,
        responses={
            200: GetFavoritesSerializer,
            400: DummyResponseSerializer,
            401: DummyResponseSerializer,
            404: DummyResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='Get favorite by id',
                value={
                          "id": 1,
                          "game": {
                            "id": 1,
                            "name": "string",
                            "year_released": 2001,
                            "genre": "string",
                            "studio": "string"
                          },
                          "user": {
                            "username": "string"
                          }
                        },
                response_only=True,
                media_type='application/json',
                status_codes=['200']
            ),
            OpenApiExample(
                name='Authentication failed',
                value={'message': 'unauthorized'},
                response_only=True,
                media_type='application/json',
                status_codes=['401']
            ),
            OpenApiExample(
                name='Given Favorite belongs to other user',
                value={'message': 'favorite with id {id} does not belong to authenticated user'},
                response_only=True,
                media_type='application/json',
                status_codes=['403']
            ),
            OpenApiExample(
                name='Favorite not found',
                value={'message': 'Favorites not found'},
                response_only=True,
                media_type='application/json',
                status_codes=['404']
            )
        ],
        summary="Get favorites",
    )
    def get(self, request, id=None):
        # id from the request is the favorite id
        is_authenticated, user = match_authenticated_user(request)
        if is_authenticated:
            try:
                favorite = Favorites.objects.get(pk=id)
                if favorite.user.id == user.id:
                    serializer = GetFavoritesSerializer(favorite)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': f'favorite with id {id} does not belong to authenticated user'}, status=status.HTTP_403_FORBIDDEN)
            except Favorites.DoesNotExist:
                return Response({'message': 'Favorites not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        request=CreateFavoriteSerializer,
        responses={
            201: DummyResponseSerializer,
            400: DummyResponseSerializer,
            401: DummyResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='Success',
                value={
                    'id': 1,
                    'game': 1,
                    'user': 1
                },
                response_only=True,
                media_type='application/json',
                status_codes=['201']
            ),
            OpenApiExample(
                name='Authorization failed',
                value={'message': 'unauthorized'},
                response_only=True,
                media_type='application/json',
                status_codes=['401']
            ),
            OpenApiExample(
                name='Bad request',
                value={'message': 'wrong input data'},
                response_only=True,
                media_type='application/json',
                status_codes=['400']
            ),
        ],
        summary="Add favorite",
    )
    def post(self, request, id=None):
        # id from the request is the game id that should be added for the user

        is_authenticated, user = match_authenticated_user(request)
        if is_authenticated:
            try:
                game = Game.objects.get(pk=id)

                favorite = Favorites.objects.filter(game=game, user=user)
                if favorite.exists():
                    return Response({'message': f'game {game.name} already added to favorites'})

                data = {
                    'game': game.id,
                    'user': user.id
                }
                serializer = CreateFavoriteSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'message': 'wrong input data'}, status=status.HTTP_400_BAD_REQUEST)
            except MultiValueDictKeyError as e:
                message = 'missing value for ' + e.args[0]
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class FavoriteAPI(APIView):

    @extend_schema(
        request=GetFavoritesSerializer,
        responses={
            200: GetFavoritesSerializer,
            401: DummyResponseSerializer,
            404: DummyResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='Get favorite by id',
                value=
                    [
                        {
                            "id": 1,
                            "game": {
                                "id": 1,
                                "name": "Baldur's Gate",
                                "year_released": 1998,
                                "genre": "RPG",
                                "studio": "BioWare"
                            },
                            "user": {
                                "username": "username"
                            }
                        },
                        {
                            "id": 1,
                            "game": {
                                "id": 1,
                                "name": "Baldur's Gate II",
                                "year_released": 2000,
                                "genre": "RPG",
                                "studio": "BioWare"
                            },
                            "user": {
                                "username": "username"
                            }
                        }
                    ],
                response_only=True,
                media_type='application/json',
                status_codes=['200']
            ),
            OpenApiExample(
                name='Authentication failed',
                value={'message': 'unauthorized'},
                response_only=True,
                media_type='application/json',
                status_codes=['401']
            ),
            OpenApiExample(
                name='Favorite not found',
                value={'message': 'Favorites not found'},
                response_only=True,
                media_type='application/json',
                status_codes=['404']
            )
        ],
        summary="Get favorites",
    )
    def get(self, request):
        is_authenticated, user = match_authenticated_user(request)
        if is_authenticated:
            try:
                favorites = Favorites.objects.filter(user=user)
                serializer = GetFavoritesSerializer(favorites, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Favorites.DoesNotExist:
                return Response({'message': 'Favorites not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)