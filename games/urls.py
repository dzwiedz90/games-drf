from django.urls import path

from . import views

app_name = 'games'
urlpatterns = [
    path('games/', views.GamesApi.as_view()),
    path('games/<int:id>/', views.GameApi.as_view()),
]