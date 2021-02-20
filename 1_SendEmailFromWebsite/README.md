# OVERVIEW

This is a project that can be installed on AWS Lightsail or AWS Elastic Beanstalk.   When setup you should be able to enter an email address in a field and then an email will be sent to that address.

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

2 - Run any necessary migrations:

```
python manage.py makemigrations
python manage.py migrate
```

3 - Run the server:

```
python manage.py runserver 8080
```

4 - Goto the localhost site:

> http://localhost:8080  
or  
> http://127.0.0.1:8080  

### TEST DJANGO ON DOCKER

---

1 - You need to be in the directory containing the Dockerfile.

2 - Run the following, using any desired replacements in the name, to build an image:

```
docker build -t mjw/sendemail .
```

3 - You should then have a docker image, you can have a look at these using the following command:

```
docker images
```

4 - Run the docker image:

```bash
docker run -p 8080:8080 mjw/sendemail
```

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

### INSTALLATION ONTO LIGHTSAIL

---

First, create a lightsail container project.   I would recommend using a Micro with a scale of 1 to ensure the costs are at a minimum to start with.

Do not setup a deployment yet, but call your service something like this:

> django-sendemail

We are going to set this up using 'My Local Machine' and there are some advanced instructions on lightsail about how to do this.

Get the domain from lightsail and update the ALLOWED_HOSTS in the settings.py file of the sendemail project.   It should look something like this:

> "django-sendemail.6hbnjaadkuqb2.eu-west-2.cs.amazonlightsail.com"

You need to create a docker image and test it as mentioned previously.

Use the following command to get the REPOSITORY and TAG for the docker image that you just created:

```
docker images
```

Now run the aws command line to push the docker image onto lightsail.   The command should look something like this:

```
aws lightsail push-container-image --region eu-west-2 --service-name django-sendemail --label sendemail --image mjw/sendemail:latest
```
(mjw/sendemail and latest were the REPOSITORY and TAG)

You should now have an image available on lightsail if you refresh the screen and it will have a name similar to the following:

> ":django-sendemail.sendemail.4"

Within lightsail, goto 'Deployments' and then 'Create your first deployment'.

Get the container a name, eg:

> "cont-sendemail"

and under the image, uset the new image that has been sent to lightsail, eg:

> ":django-sendemail.sendemail.4"

Add an open port of 8080 to HTTP.

Within your public endpoint, select your container name from the combo box, eg:

> "cont-sendemail"

Hit save and deploy and then wait for it to finish deploying.

Once it has finished deploying, you should be able to follow your public domain link from lightsail and see the website working on the other end.

### INSTALLATION ONTO ELASTIC BEANSTALK

---

Firstly, move into the directory where the Dockerfile is located.

This installation does not use Dockerhub or any other repository to make the installation simple, however it is dependent upon the Dockerrun.aws.json file in the remote-docker directory, so I suggest you take a look at this.

You then need to initiate an Elastic Beanstalk App using a command similar to the following:

```
eb init -i -p docker contSendEmailApp
```

You may be asked to select some setup details such as which region you want to set this up in and if you want to use an SSH key.   Check AWS Elastic Beanstalk to ensure the App has been created.

You can now test the docker image in your local environment by using the following command:

```
eb local run --port 8080
```

Check the localhost to ensure the website displays correctly:

> http://localhost:8080  
  
> http://127.0.0.1:8080  

Next you need to create an Elastic Beanstalk environment by running something similar to the following:

```
eb create contsendemail-env
```

Check Elastic Beanstalk to ensure the environment is created successfully.

You will need to either get the domain name from elastic beanstalk or use the following command to get the domain name:

```
eb open
```

Then update the LOCAL_HOSTS in the settings.py file of the sendemail project with the appropriate domain from the elastic beanstalk environment, eg:

> "contsendemail-env.eba-kihs3gqn.eu-west-2.elasticbeanstalk.com"

Then redeploy using the following command:

```
eb deploy
```

You can now open the website from Elastic Beanstalk, or use the following command:

```
eb open
```

This method of creating an elastic beanstalk environment will create a load balanced environment by default, which can be expensive, so I suggest you change the configuration quickly.   You may also wish to play around with what ec2 instances are used etc.

### INSTALLATION ONTO ELASTIC BEANSTALK

---

The Elastic Beanstalk installation creates a set of directories and files that you can delete if you remove the Elastic Beanstalk environment and app:

.elasticbeanstalk  
.dockerignore  
.gitignore  

This project also has a tendency to leave docker images and containers around, so these basic commands may be useful:

```
docker ps -a
docker stop containerid_or_name
docker rm containerid_or_name
docker images
docker rmi imagename
```

Don't forget to delete the Elastic Beanstalk and/or Lightsail environment if you don't use it.   They may be costing you money.