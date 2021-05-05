# WARNING - DOCKER IMAGES CAN TAKE UP A LOT OF ROOM

# This has been tested and works but produces an image of 1.01GB
# FROM python:3.8-buster

# This has been tested and works, but requires the apk update line below and
# produces an image of 345 MB.   This is smaller than the PostgreSQL image in
# the github history.
FROM python:3.8-alpine

RUN apk update && apk add \
        git openssh \
        libuuid \
        pcre \
        mailcap \
        gcc \
        libc-dev \
        linux-headers \
        pcre-dev \
        tzdata \
    && pip install --no-cache-dir uWSGI \
    && rm -rf /tmp/*

RUN apk add --no-cache --virtual .build-deps mariadb-dev \
    && pip install mysqlclient \
    #&& apk add --no-cache mariadb-client-libs \
    #&& apk del .build-deps \
    && apk del \
        gcc \
        libc-dev \
        linux-headers

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


EXPOSE 8080

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Do not change the 0.0.0.0, but use localhost or 127.0.0.1 to view
# the site.

# Choose which method to use:
ENTRYPOINT python3 manage.py collectstatic --noinput; \
python3 manage.py makemigrations; \
python3 manage.py migrate; \
gunicorn --bind 0.0.0.0:8080 --workers 3 brokerdata.wsgi