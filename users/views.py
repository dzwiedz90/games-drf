from django.contrib.auth.hashers import check_password
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Favorites
from .serializers import CreateGameSerializer, GetFavoritesSerializer
from games.models import Game
from utils.utils import match_authenticated_user

class AuthApi(APIView):
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
    def post(self, request):
        try:
            if request.data:
                data = request.data
                User.objects.create_user(username=data['username'], password=data['password'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
                return Response({'message': 'user created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'missing POST data'}, status=status.HTTP_401_UNAUTHORIZED)
        except MultiValueDictKeyError as e:
            message = 'missing value for ' + e.args[0]
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

class FavoritesApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None):
        # id from the request is the favorite id
        is_authenticated, user = match_authenticated_user(request)
        if is_authenticated:
            if id is None:
                try:
                    favorites = Favorites.objects.filter(user=user)
                    serializer = GetFavoritesSerializer(favorites, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Favorites.DoesNotExist:
                    return Response({'message': 'Favorites not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
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
                serializer = CreateGameSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({'message': 'wrong input data'}, status=status.HTTP_400_BAD_REQUEST)
            except MultiValueDictKeyError as e:
                message = 'missing value for ' + e.args[0]
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)