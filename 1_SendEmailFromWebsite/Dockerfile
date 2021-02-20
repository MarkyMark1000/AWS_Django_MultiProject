FROM python:3.10.0a5-alpine3.12

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

EXPOSE 8080

# RUN apk add --update py3-pip

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN python3 /code/manage.py makemigrations

RUN python3 /code/manage.py migrate

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "sendemail.wsgi"]