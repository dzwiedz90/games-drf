from django.db import models

class Game(models.Model):
    name = models.CharField('name', max_length=64)
    year_released = models.IntegerField("year_released")
    genre = models.CharField("genre", max_length=64)
    studio = models.CharField("studio", max_length=64)
