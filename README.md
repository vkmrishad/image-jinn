# image-jinn
High-performance image storage service

![example workflow](https://github.com/vkmrishad/image-jinn/actions/workflows/black.yaml/badge.svg?branch=main)
![example workflow](https://github.com/vkmrishad/image-jinn/actions/workflows/django-ci.yaml/badge.svg?branch=main)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This system is build over s3 storage which is scalable and reliable.

## Clone

    git clone https://github.com/vkmrishad/image-jinn.git
    or
    git clone git@github.com:vkmrishad/image-jinn.git

## System dependencies

* [Python: 3.8+](https://www.python.org/downloads/)
* [PostgreSQL: 12+](https://www.postgresql.org/download/)
* [Redis: 6+](https://redis.io/docs/getting-started/installation/)
* [Minio (Simulate AWS S3)](https://min.io/download)

## Environment and Package Management
Install [Poetry](https://python-poetry.org/)

    $ pip install poetry
    or
    $ pip3 install poetry

Activate or Create Env

    $ poetry shell

Install Packages from Poetry

    $ poetry install

NB: When using virtualenv, install from [requirements.txt](/requirements.txt) using `$ pip install -r requirements.txt`.
For environment variables follow [sample.env](/sample.env)

## Runserver

    $ python manage.py runserver
    or
    $ ./manage.py runserver

## Run Celery

    $ celery -A image_jinn  worker -l info

## Runserver using docker
Check this documentation to run with [docker](https://docs.docker.com/desktop/), refer [link](https://docs.docker.com/samples/django/)
Create .env file in project folder and copy all ENV vars without having `export`.

For initial db setup add, postgres ENV vars
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
You can use your own values, Please use `DATABASE_HOST='postgres'` for docker settings only

    $ docker-compose build
    $ docker-compose up

For shutting down use,

    $ docker-compose down

Apply migration to database

    $ docker-compose exec app python manage.py migrate

#### Access server: http://127.0.0.1:8000
#### Access Admin: http://127.0.0.1:8000/admin/

## API Endpoints
Check Swagger/Redoc documantation after running server
#### Swagger: http://127.0.0.1:8000/api/
#### Redoc: http://127.0.0.1:8000/redoc/

## Test
For testing, moto_server need to be run in a new tab or background. For running moto_server, Flask is required and added in requirements.txt.

    $ moto_server

moto_server will be running on http://127.0.0.1:5000, then run test

    $ python manage.py test apps
    or
    $ ./manage.py test apps

## Create superuser
Create superuser to test admin feature

    $ python manage.py createsuperuser
    or
    $ ./manage.py createsuperuser
