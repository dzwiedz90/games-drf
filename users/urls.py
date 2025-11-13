from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('users/auth/', views.AuthApi.as_view()),
    path('users/auth/register/', views.AuthApiRegistration.as_view()),
    path('users/favorites/', views.FavoritesApi.as_view()),
    path('users/favorites/<int:id>/', views.FavoritesApi.as_view()),
]