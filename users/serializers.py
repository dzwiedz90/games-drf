from rest_framework import serializers

from .models import Favorites, User
from games.serializers import GetGameSerializer

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class GetFavoritesSerializer(serializers.ModelSerializer):
    game = GetGameSerializer(read_only=True)
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'game', 'user']

class CreateFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'game', 'user']

class DummyAuthApiRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text='username')
    password = serializers.CharField(help_text='password')

class DummyResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text='response message')

class DummyAuthRegisterRequestSerializer(serializers.Serializer):
    username =  serializers.CharField(help_text='username')
    password =  serializers.CharField(help_text='password')
    email =  serializers.CharField(help_text='email')
    first_name =  serializers.CharField(help_text='first_name')
    last_name = serializers.CharField(help_text='last_name')
