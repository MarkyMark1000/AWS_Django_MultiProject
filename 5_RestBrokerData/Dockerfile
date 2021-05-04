# WARNING - DOCKER IMAGES CAN TAKE UP A LOT OF ROOM

# This has been tested and works but produces an image of 1.01GB
# FROM python:3.8-buster

# This has been tested and works, but requires the apk update line below and
# produces an image of 584 MB.
FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# I could not get the slim versions to work at present.   I would need to go
# through the postgre installation.   It might be better if using numpy and
# are worried about security.   see:
# https://towardsdatascience.com/how-to-build-slim-docker-images-fast-ecc246d7f4a7


# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# I have found that lightsail doesn't seem to pass in environment
# variables to the container effectively, but it does work with EB.
# The following line gets the Environment Variable, HOWEVER
# DJANGO_DEBUG IS NOT CURRENTLY USED.   PLEASE SEE THE ENTRYPOINT
# LINE.


# Echo the Environment variables to help with debugging
ARG DJANGO_DEBUG
ARG API_ENVIRONMENT
ENV DJANGO_DEBUG=${DJANGO_DEBUG}
ENV API_ENVIRONMENT=${API_ENVIRONMENT}

EXPOSE 8080

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN python3 manage.py collectstatic --noinput

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

# Do not change the 0.0.0.0, but use localhost or 127.0.0.1 to view
# the site.

# Choose which method to use:
ENTRYPOINT gunicorn --bind 0.0.0.0:8080 --workers 3 brokerdata.wsgi