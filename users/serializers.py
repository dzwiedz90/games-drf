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

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'game', 'user']
