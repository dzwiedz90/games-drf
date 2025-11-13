from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from.managers import CustomUserManager
from games.models import Game

class User(AbstractBaseUser):
    username = models.CharField('username', max_length=64, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField('first_name', max_length=64)
    last_name = models.CharField('last_name', max_length=64)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

class Favorites(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)