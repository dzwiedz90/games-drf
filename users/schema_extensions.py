from drf_spectacular.utils import OpenApiExample

from users.serializers import DummyAuthApiRequestSerializer, DummyResponseSerializer, \
    DummyAuthRegisterRequestSerializer, GetFavoritesSerializer, CreateFavoriteSerializer

auth_api_schema = {
    "request": DummyAuthApiRequestSerializer,
    "responses": {
        200: DummyResponseSerializer,
        400: DummyResponseSerializer,
        401: DummyResponseSerializer,
        404: DummyResponseSerializer,
    },
    "examples": [
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
    "summary": "Log in registered user"
}

auth_api_registration_schema = {
    "request": DummyAuthRegisterRequestSerializer,
    "responses": {
        200: DummyResponseSerializer,
        400: DummyResponseSerializer,
    },
    "examples": [
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
    "summary": "Register a new user",
}

get_favorites_api_schema = {
    "request": GetFavoritesSerializer,
    "responses": {
        200: GetFavoritesSerializer,
        400: DummyResponseSerializer,
        401: DummyResponseSerializer,
        404: DummyResponseSerializer,
    },
    "examples": [
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
    "summary": "Get favorites"
}

post_favorites_api_schema = {
    "request": CreateFavoriteSerializer,
    "responses": {
        201: DummyResponseSerializer,
        400: DummyResponseSerializer,
        401: DummyResponseSerializer,
    },
    "examples": [
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
    "summary": "Add favorite"
}

get_favorite_api_schema = {
    "request": GetFavoritesSerializer,
    "responses": {
        200: GetFavoritesSerializer,
        401: DummyResponseSerializer,
        404: DummyResponseSerializer,
    },
    "examples": [
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
    "summary": "Get favorites"
}