# Simple posts app

Objective of this task is to create a simple REST API based social network in Django where Users can sign up and create text posts, as well as view, like, and unlike other Users’ posts.

Functional requirements:
* on signup, validate email formatting and only allow signups with valid emails 
* once signed up, enrich the User with geolocation data of the IP that the signup originated from 
* based on geolocation of the IP, check if the signup date coincides with a holiday in the User’s country, and save that info 

Technical requirements:
* use JWT for user authentication 
* data enrichment must be performed asynchronously, i.e. independently of the signup route API request processing 
* API endpoints functionality must be suitably covered with tests 
* use django-rest-framework library for API 
* implement retries for requests towards 3rd party API

## Getting Started for local usage

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).
```
1) virtualenv venv
2) source project-env/bin/activate
3) pip install -r requirements.txt
```
Setup Env Variables. Create .env file along-side manage.py module

|    NAME   |                      DESCRIPTION                      |DEFAULT VALUE|
|-----------|-------------------------------------------------------|-------------|
|DEBUG      |Debug mode for local machine, set `False` on porduction|     False    |
|SECRET_KEY |Secret key for encrypting password and etc secure value|  - |
|SQL_ENGINE |Configuration str, what db do you use| `django.db.backends.sqlite3` |
|SQL_DATABASE |Name of your db | `sqlite3.db` |
|SQL_USER |Name of db user | user
|SQL_PASSWORD |DB password | password |
|SQL_HOST | DB host | localhost |
|SQL_PORT | DB port | 5432 |
|ALLOWED_HOSTS |  | [] |
|EMAIL_API_KEY | api key from https://www.abstractapi.com/ for validating email| - |
|IP_API_KEY | api key from https://www.abstractapi.com/ for getting ip info | - |
|HOLIDAYS_API_KEY | api key from https://www.abstractapi.com/ for getting info about holidays based on country | - |
|CELERY_BROKER_URL | redis url ex: redis://localhost:6379 | - |
|CELERY_RESULT_BACKEND | redis url ex: redis://localhost:6379 | - |

Make sure that redis is up to running.
Run redis on terminal: ```redis-server``` 
```
5) python manage.py migrate 
6) python manage.py runserver 
```

## Tests
Tests can be run:
```python manage.py test```

## Dependencies

* Django==4.0.3
* django-environ==0.8.1
* djangorestframework==3.13.1
* djangorestframework-simplejwt==5.1.0
* requests==2.27.1 # <em>for making requests to 3rd party services</em>
* celery==5.2.6 # <em>for asynchronous tasks on background</em>
* redis==4.2.2  # <em>used as a message broker for celery</em>
* drf-yasg==1.20.0 # <em>for auto generation API docs. url .../swagger/</em>

## Authors

* **Almaz Yusupov** - [Almaz97](https://github.com/Almaz97)