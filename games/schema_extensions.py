from drf_spectacular.utils import OpenApiExample, OpenApiParameter

from games.serializers import GetGameSerializer, DummyResponseSerializer, CreateGameSerializer

get_games_api_schema = {
    "parameters": [
        OpenApiParameter(
            name='genre',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Gatunek gry',
            required=False,
            default='RPG'
        ),
        OpenApiParameter(
            name='year_released',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Rok wydania gry',
            required=False,
            default=1999
        )
    ],
    "responses": {
        200: GetGameSerializer,
        400: DummyResponseSerializer,
        401: DummyResponseSerializer,
        404: DummyResponseSerializer,
    },
    "examples": [
        OpenApiExample(
            name='Get all games paged, possible filtration by genre or year_released',
            value={
                "count": 44,
                "next": "http://baseurl/games/?page=2",
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "Baldur's Gate II",
                        "year_released": 2000,
                        "genre": "RPG",
                        "studio": "BioWare"
                    },
                    {
                        "id": 2,
                        "name": "Super Mario Bros",
                        "year_released": 1985,
                        "genre": "platformowa",
                        "studio": "Nintendo"
                    },
                    {
                        "id": 3,
                        "name": "Gothic",
                        "year_released": 2001,
                        "genre": "RPG",
                        "studio": "Piranha Bytes"
                    }
                ]
            },
            response_only=True,
            media_type='application/json',
            status_codes=['200']
        ),
        OpenApiExample(
            name='Login failed, credentials not valid',
            value={'message': 'unauthorized'},
            response_only=True,
            media_type='application/json',
            status_codes=['401']
        ),
        OpenApiExample(
            name='Bad request',
            value={'message': 'missing value for genre'},
            response_only=True,
            media_type='application/json',
            status_codes=['400']
        )
    ],
    "summary": "Get all games paged"
}

post_games_api_schema = {
    "request": CreateGameSerializer,
    "responses": {
        200: CreateGameSerializer,
        400: DummyResponseSerializer,
        401: DummyResponseSerializer,
        404: DummyResponseSerializer,
    },
    "examples": [
        OpenApiExample(
            name='Add new game',
            value={
                "id": 10,
                "name": "Game",
                "year_released": 2000,
                "genre": "cRPG",
                "studio": "Somestudio"
            },
            response_only=True,
            media_type='application/json',
            status_codes=['200']
        ),
        OpenApiExample(
            name='Login failed, credentials not valid',
            value={'message': 'unauthorized'},
            response_only=True,
            media_type='application/json',
            status_codes=['401']
        ),
        OpenApiExample(
            name='Bad request',
            value={'message': 'missing value for genre'},
            response_only=True,
            media_type='application/json',
            status_codes=['400']
        )
    ],
    "summary": "Add new game"
}

get_game_api_schema = {
    "responses": {
                200: GetGameSerializer,
                401: DummyResponseSerializer,
                404: DummyResponseSerializer,
            },
    "examples": [
        OpenApiExample(
            name='Add new game',
            value={
                "id": 10,
                "name": "Game",
                "year_released": 2000,
                "genre": "cRPG",
                "studio": "Somestudio"
            },
            response_only=True,
            media_type='application/json',
            status_codes=['200']
        ),
        OpenApiExample(
            name='Login failed, credentials not valid',
            value={'message': 'unauthorized'},
            response_only=True,
            media_type='application/json',
            status_codes=['401']
        ),
        OpenApiExample(
            name='Bad request',
            value={'message': 'game with the id 123 does not exist'},
            response_only=True,
            media_type='application/json',
            status_codes=['404']
        )
    ],
    "summary": "Get games by id"
}