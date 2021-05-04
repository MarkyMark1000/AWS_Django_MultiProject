# OVERVIEW

This project represents a REST API that I would like to use to collect broker data such as
spread, stoplevel and freezelevel.

There are 2 main apps, the backend and frontend because I don't want to use seperate apps.   At present, there isn't much to the frontend and it needs work.

I have been experimenting with Dockerfiles, postgresql and MySQL, so you may wish to look at the
history at different versions of the Dockerfile.


### MAKEFILE

---

A makefile has been created to help simplify the running of repetitive commands.   It can be used to clean the environment, create a new virtual environment, run the code locally and run the code within Docker.:

> make

> make help

You may need to regularly clean up docker images and containers if you use this extensively.   The makefile does not currently install or deploy this project to Lightsail or Elastic Beanstalk.

### SETUP

This project uses a file stored in the following location, which I have not copied onto github and will need to be created:

> ./brokerdata/extra_code_or_config/hidden_account.py

The file should take the following format:

```python
# Live DB:
LIVE_DB_NAME = 'dbBrokerData'
LIVE_DB_USER = 'broker_admin'
LIVE_DB_PASSWORD = '....'
LIVE_DB_HOST = '.....'
LIVE_DB_PORT = '5432'
# Test DB:
TEST_DB_NAME = 'dbBrokerData'
TEST_DB_USER = '....'
TEST_DB_PASSWORD = '....'
TEST_DB_HOST = '....'
TEST_DB_PORT = '5432'
# Docker DB:
DOCK_DB_NAME = 'dbBrokerData'
DOCK_DB_USER = '....'
DOCK_DB_PASSWORD = '.....'
DOCK_DB_HOST = 'host.docker.internal'
DOCK_DB_PORT = '5432'
```

### TEST DJANGO LOCALLY

---

To test the django site locally, follow these instructions:

1 - If necessary delete and rebuild the venv virtual environment using the requirements.txt file:

```
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

2 - Set Django Debug to True or False.

```
export DJANGO_DEBUG='False'
export API_ENVIRONMENT='Local'
```

3 - Collect the static files:

```
python3 manage.py collectstatic --noinput
```
(files are copied to staticfiles directory)

4 - Run any necessary migrations:

```
python manage.py makemigrations
python manage.py migrate
```

5 - Run the server:

```
python manage.py runserver 8080 --nostatic
```
(--nostatic, ensures server is consistent with whitenoise.   If you wish to see the site on your local network use 0.0.0.0:8080 instead of 8080.   The ip address will be listed out automatically.)

6 - Goto the localhost site:

> http://localhost:8080  
or  
> http://127.0.0.1:8080

### TEST DJANGO ON DOCKER

---

1 - You need to be in the directory containing the Dockerfile.

2 - Run the following, using any desired replacements in the name, to build an image:

```
docker build --build-arg DJANGO_DEBUG=True --build-arg API_ENVIRONMENT=Docker -t mjw/brokerdata .
```

3 - You should then have a docker image, you can have a look at these using the following command:

```
docker images
```

4 - Run the docker image:

```bash
docker run -p 8080:8080 mjw/brokerdata
```
(*Please read the Dockerfile because DJANGO_DEBUG may not work depending upon how you set this file up.*)

5 - Then look at the appropriate localhost site:

> http://localhost:8080  
or  
> http://127.0.0.1:8080  

6 - I suggest you clean up any docker images or docker containers as you go along.   This is easy using the Dashboard on a mac, but you could use the following commands:

```
docker ps -a
docker stop containerid_or_name
docker rm containerid_or_name
docker images
docker rmi imagename
```
---
