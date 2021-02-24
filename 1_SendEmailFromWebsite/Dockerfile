FROM python:3.10.0a5-alpine3.12

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Environment Variables Passed Into the Container
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

# When you upload a django container to lightsail, you have limited
# access to the proxy server and so it is difficult to configure the
# static files.

# It may be possible to get around this by using a custom load balancer:
# https://aws.amazon.com/blogs/compute/deploying-an-nginx-based-http-https-load-balancer-with-amazon-lightsail/

# Do not change the 0.0.0.0, but use localhost or 127.0.0.1 to view
# the site.

# Choose which method to use:
# ENTRYPOINT ["python3", "/code/manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT gunicorn --bind 0.0.0.0:8080 --workers 3 sendemail.wsgi