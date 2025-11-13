from rest_framework import serializers

from .models import Game


class GetGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'year_released', 'genre', 'studio']
