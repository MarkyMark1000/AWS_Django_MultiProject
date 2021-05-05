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

---

##### DATABASE

---

This current project is dependent upon MySQL server (a postgresql version exists in the github history), so you will need to setup a local server and a production server for use on AWS.

It would be wise to create a specific database and user for this system and example sql can be found below:

```SQL
CREATE DATABASE dbBrokerData;
CREATE DATABASE test_dbBrokerData;
```
To create a new user use one of the following and make appropriate adjustments:
```SQL
CREATE USER 'broker_admin'@'%' IDENTIFIED BY '.......';
```
Other commands that may be useful:
```SQL
USE dbBrokerData
GRANT ALL PRIVILEGES ON dbBrokerData.* TO 'broker_admin'@'%';
USE test_dbBrokerData
GRANT ALL PRIVILEGES ON test_dbBrokerData.* TO 'broker_admin'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'broker_admin'@'%';
```

##### CODE

---
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

7 - It is possible to build a docker image for deployment.   A suitable make command exists, but you could also use the following:

```
docker build --build-arg DJANGO_DEBUG=False --build-arg API_ENVIRONMENT=Prod -t mjw/brokerdata .
```

### INSTALLATION ONTO LIGHTSAIL

---

###### WARNING

---

Deploying containers in AWS can take up significant memory or be expensive if  you use a large instance.   Some of the following commands may be useful if you run into problems:

```
sudo su -
free -m
cat /proc/meminfo
vmstat -s
docker ps -a
docker logs -f <Container ID>
docker stats
```


You will also probably want to Enable 'session persistance' for this application.   I believe this is refered to as 'stickiness' in Elastic Beanstalk.   More information on stickiness can be found here:

> https://lightsail.aws.amazon.com/ls/docs/en_us/articles/enable-session-stickiness-persistence-or-change-cookie-duration

You will also want to ensure that lightsail has access to RDS if you are using a database there.   Example adjustments to access a database on RDS can be found in the following link:

> https://aws.amazon.com/blogs/compute/amazon-lightsail-database-tips-and-tricks/

###### OVERVIEW

---

First, create a lightsail container project.   I would recommend using a Micro with a scale of 1 to ensure the costs are at a minimum to start with.

Do not setup a deployment yet, but call your service something like this:

> django-brokerdata

We are going to set this up using 'My Local Machine' and there are some advanced instructions on lightsail about how to do this.

Get the domain from lightsail and update the ALLOWED_HOSTS in the settings.py file of the basiclogin project.   It should look something like this:

> "django-brokerdata.6hbnjaadkuqb2.eu-west-1.cs.amazonlightsail.com"

You need to create a docker image and test it as mentioned previously.

```
docker build -t mjw/brokerdata .
```
```
docker run -e DJANGO_DEBUG=True -e API_ENVIRONMENT=Docker -p 8080:8080 mjw/brokerdata
```


Use the following command to get the REPOSITORY and TAG for the docker image that you just created:

```
docker images
```

As this system access a database on RDS, you need to enable VPC Peering on lightsail (Amazon Lightsail -> Account/Account -> Advanced -> VPC Peering)

You also need to ensure the database is accessible from lightsail and it could be worth enabling stickyness.   See the links mentioned above in the warning section !

Now run the aws command line to push the docker image onto lightsail.   The command should look something like this:

```
aws lightsail push-container-image --region eu-west-2 --service-name django-brokerdata --label brokerdata --image mjw/brokerdata:latest
```
(*mjw/brokerdata and latest were the REPOSITORY and TAG*)

You should now have an image available on lightsail if you refresh the screen and it will have a name similar to the following:

> ":django-brokerdata.brokerdata.4"

Within lightsail, goto 'Deployments' and then 'Create your first deployment'.

Give the container a name, eg:

> "cont-brokerdata"

and under the image, set the new image that has been sent to lightsail, eg:

> ":django-brokerdata.brokerdata.4"

Add an open port of 8080 to HTTP.

Don't forget to add suitable environment variables such as:

> DJANGO_DEBUG=False  
> API_ENVIRONMENT=Prod  

Within your public endpoint, select your container name from the combo box, eg:

> "cont-brokerdata"

Hit save and deploy and then wait for it to finish deploying.

Once it has finished deploying, you should be able to follow your public domain link from lightsail and see the website working on the other end.

---