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
## Endpoints

http://{base_url}/swagger/
