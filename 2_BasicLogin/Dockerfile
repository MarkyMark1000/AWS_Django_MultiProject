FROM python:3.10.0a5-alpine3.12

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# I have found that lightsail doesn't seem to pass in environment
# variables to the container effectively, but it does work with EB.
# The following line gets the Environment Variable, HOWEVER
# DJANGO_DEBUG IS NOT CURRENTLY USED.   PLEASE SEE THE ENTRYPOINT
# LINE.
ENV DJANGO_DEBUG=$DJANGO_DEBUG

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
# ENTRYPOINT export DJANGO_DEBUG='True'; python3 /code/manage.py runserver 0.0.0.0:8080
ENTRYPOINT export DJANGO_DEBUG='True'; gunicorn --bind 0.0.0.0:8080 --workers 3 basiclogin.wsgi