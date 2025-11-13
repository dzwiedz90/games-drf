# Games API DRF
--------------
--------------

## Technologies used
- Python 3.11
- Django 5.2.8
- django-filter 25.2
- djangorestframework 3.16.1
- python-dotenv 1.2.1

### Configuration before first run:
- download master from repo
- configure virtual environment in Python:
- install modules from requirements.txt
- create .env file in root folder where manage.py file is and save SECRET_KEY inside
- make django migrations:
  - python manage.py makemigrations
  - python manage.py migrate
- create super user
- load fixttures:
  - python3 manage.py loaddata games/fixtures/games.json --app app.Game
- run django server
---
## Authorization

One should set a header 
### --header 'Authorization: Token token'
in the request.</br>
All endpoints require user to authenticate themself.

---
## Endpoints

---
## Users

### POST users/auth/register/
Endpoint used to register a new user</br>
Request:
```bash
curl --location '{base_url}/users/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "username",
    "password": "password",
    "email": "test@test.com",
    "first_name": "Name",
    "last_name": "Lastname"
}'
```
Response:
```json
{
    "message": "user created"
}
```

### POST users/auth/
Endpoint used to authenticate and get token, requires user's username and password</br>
Request:
```bash
curl --location '{base_url}/users/auth/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "username",
    "password": "password"
}'
```
Response:
```json
{
    "message": "Token token"
}
```

### GET users/favorites/
Endpoint used to get a list of favorite games for authenticated user</br>
Request:
```bash
curl --location '{base_url}/users/favorites/' \
--header 'Authorization: Token token' \
--data ''
```

Response:
```json
[
    {
        "id": 11,
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
]
```

### GET users/favorites/<int:id>/
Endpoint used to get a favorite game by id, user can obtain only favorites associated with his account</br>
Request:
```bash
curl --location '{base_url}/users/favorites/{id}/' \
--header 'Authorization: Token token' \
--data ''
```

Response:
```json
{
    "id": 11,
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
```

### POST users/favorites/<int:id>/
Endpoint used to add a game to favourites for the authenticated user</br>
Request:
```bash
curl --location --request POST '{base_url}/users/favorites/{id}/' \
--header 'Authorization: Token token' \
--data ''
```
Response:
```json
{
    "id": 1,
    "game": 1,
    "user": 1
}
```

---
## Games

### GET games/
Endpoint used to retrieve list of all games. Results are paged and can be filtered by fields genre and year_released</br>
Request:
```bash
curl --location '{bas_url}/games/' \
--header 'Authorization: Token token' \
--data ''
```
Response:
```json
{
    "count": 44,
    "next": "http://baseurl/games/?page=2",
    "previous": null,
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
}
```

### POST games/
Endpoint used add a new game</br>
Request:
```bash
curl --location '{base_url}/games/' \
--header 'Authorization: Token token' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Game",
    "year_released": "2000",
    "genre": "cRPG",
    "studio": "Somestudio"
}'
```

Response:
```json
{
    "id": 10,
    "name": "Game",
    "year_released": 2000,
    "genre": "cRPG",
    "studio": "Somestudio"
}
```

### POST games/<int:id>/
Endpoint used retrieve a game by given id</br>
Request:
```bash
curl --location '{base_url}}/games/7/' \
--header 'Authorization: Token token' \
--data ''
```
Response:
```json
{
    "id": 7,
    "name": "Warcraft III",
    "year_released": 2002,
    "genre": "RTS",
    "studio": "Blizzard"
}
```

