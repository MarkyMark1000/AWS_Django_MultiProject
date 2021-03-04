# OVERVIEW

This is a project that can be installed on AWS Lightsail or AWS Elastic Beanstalk.   It is designed around the use of Django containers, not the Django or Python environments available on these platforms.   When setup you should be able to enter an email address in a field and then an email will be sent to that address.

### NOTES FOR THIS PROJECT

---

- Password Validators in the settings.py file.
- Create a superuser
- Mention I found difficult without password validator and didn't
  like the default ones, so wrote my own.
- I believe problems exists if you don't use Profile model.
- Mention following tutorial:
  https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m



### A NOTE ON STATIC FILES

---

When using AWS it is possible to specify options for the Django or Python environments to specify where to get the static files.   This is not available for the deployment of containers onto Lightsail or Elastic Beanstalk.   I have spent some time trying to get around this and tried the following:

- Adjusting Nginx and .ebextensions to enable static file deployment from a different folder.
- Adding the static files to an S3 instance.

After some trial and error, I found that the use of whitenoise is much easier to setup and so decided to progress with this option.   It creates new file versions when necessary and deploys static files effectively.

Please note that DJANGO_DEBUG must be set to False for this to work properly, otherwise it does not deploy the versioned files.

There are also some adjustments made to the settings.py file to get this to work.  

The collected static files are saved in the 'staticfiles' directory.

Please see the following:

> http://whitenoise.evans.io/en/stable/

> http://whitenoise.evans.io/en/stable/django.html

---

### AWS SETUP

---

This project uses AWS SES (Simple Email Service) to send an email.   As such there are some security and setup considerations that need to be considered.

- Elastic Beanstalk may not have access to SES and you may need to adjust the role (see elastic beanstalk environment -> configuration -> security) within IAM so that the EC2 instance can access SES.

- You may need to make some setup adjustments within LightSail to gain access to SES.
   > https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-how-to-set-up-vpc-peering-with-aws-resources

- It is worth noting that SES does not necessarily send and receive emails in every region.   This code uses eu-west-1 (Ireland) because the code is replicated from another application which I have setup and works well for sending and receiving emails.   It is worth reviewing this list of acceptable email domains within the following link:
   > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/regions.html

- AWS May limit who you can send emails to.   You may need to research Sandbox and sending limit's in the following section:
   > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/regions.html


- There is lots more information on SES in the following link:
   > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html

- It is possible to make the application work from your local computer if the local configuration for the AWS CLI has been setup.   However, if you run the docker containers locally, they may not work when hitting the send button.   These links may be helpful:
   > https://stackoverflow.com/questions/40415943/how-to-see-what-profile-is-default-with-cli
   > https://www.thegeekstuff.com/2019/03/aws-configure-examples/

### MAKEFILE

---

A makefile has been created to help simplify the running of the following sections:

> TEST DJANGO LOCALLY

> TEST DJANGO ON DOCKER

It does not currently install or deploy this project to Lightsail or Elastic Beanstalk.

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

2 - Set Django Debug to False.

```
export DJANGO_DEBUG='False'
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
(--nostatic, ensures server is consistent with whitenoise)

6 - Goto the localhost site:

> http://localhost:8080  
or  
> http://127.0.0.1:8080

### TEST DJANGO ON DOCKER

---

1 - You need to be in the directory containing the Dockerfile.

2 - Run the following, using any desired replacements in the name, to build an image:

```
docker build -t mjw/basiclogin .
```

3 - You should then have a docker image, you can have a look at these using the following command:

```
docker images
```

4 - Run the docker image:

```bash
docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/basiclogin
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
---

### INSTALLATION ONTO LIGHTSAIL

---

First, create a lightsail container project.   I would recommend using a Micro with a scale of 1 to ensure the costs are at a minimum to start with.

Do not setup a deployment yet, but call your service something like this:

> django-basiclogin

We are going to set this up using 'My Local Machine' and there are some advanced instructions on lightsail about how to do this.

Get the domain from lightsail and update the ALLOWED_HOSTS in the settings.py file of the basiclogin project.   It should look something like this:

> "django-basiclogin.6hbnjaadkuqb2.eu-west-1.cs.amazonlightsail.com"

You need to create a docker image and test it as mentioned previously.

```
docker build -t mjw/basiclogin .
```
```  
docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/basiclogin
```

Use the following command to get the REPOSITORY and TAG for the docker image that you just created:

```
docker images
```

Now run the aws command line to push the docker image onto lightsail.   The command should look something like this:

```
aws lightsail push-container-image --region eu-west-1 --service-name django-basiclogin --label basiclogin --image mjw/basiclogin:latest
```
(mjw/basiclogin and latest were the REPOSITORY and TAG)

You should now have an image available on lightsail if you refresh the screen and it will have a name similar to the following:

> ":django-basiclogin.basiclogin.4"

Within lightsail, goto 'Deployments' and then 'Create your first deployment'.

Give the container a name, eg:

> "cont-basiclogin"

and under the image, uset the new image that has been sent to lightsail, eg:

> ":django-basiclogin.basiclogin.4"

Add the following environment variables:

> DJANGO_DEBUG => False

Also, add an open port of 8080 to HTTP.

Within your public endpoint, select your container name from the combo box, eg:

> "cont-basiclogin"

Hit save and deploy and then wait for it to finish deploying.

Once it has finished deploying, you should be able to follow your public domain link from lightsail and see the website working on the other end.

---

### INSTALLATION ONTO ELASTIC BEANSTALK

---

###### OVERVIEW

---

Firstly, move into the directory where the Dockerfile is located.

This installation does not use Dockerhub or any other repository to make the installation simple, however it is dependent upon the Dockerrun.aws.json file in the remote-docker directory, so I suggest you take a look at this.  

This Elastic Beanstalk installation procedure may add the following files and directories.   They can be deleted to clean things up, but it is worth checking the files to ensue that when you re-deploy, you send it to the correct region, environment etc:
- .elasticbeanstalk  
- .dockerignore  
- .gitignore

###### SETUP AND DEPLOYMENT

---

Initiate an Elastic Beanstalk App using a command similar to the following:

```
eb init -i -p docker contBasicLoginApp
```

You may be asked to select some setup details such as which region you want to set this up in and if you want to use an SSH key.   Check AWS Elastic Beanstalk to ensure the App has been created.

You can now test the docker image in your local environment by using the following command:

```
eb local run --envvars DJANGO_DEBUG="False" --port 8080
```

Check the localhost to ensure the website displays correctly:

> http://localhost:8080  
  
> http://127.0.0.1:8080  

If you are re-deploying code to Elastic Beanstalk, I suggest you check the .elasticbeanstalk/config.yaml file to ensure the environment you are deploying to is correct.  

Either create a new Elastic Beanstalk or deploy to an existing environment using the appropriate command from the following:

```
eb create contbasiclogin-env
```

```
eb deploy
```

If you have created the environment for the first time, you will need to update the LOCAL_HOSTS in the settings.py file of the basiclogin project with the appropriate domain from the elastic beanstalk environment, eg:

> "contbasiclogin-env.eba-kihs3gqn.eu-west-1.elasticbeanstalk.com"

Within the .ebextensions directory, there is a file called environment.config.   This file initiates the DJANGO_DEBUG variable, so you may want to change this value depending on if you want to initiate the project in debug or production mode.

If necessary, redeploy using the following command:

```
eb deploy
```

You can now open the website from Elastic Beanstalk, or use the following command:

```
eb open
```

This method of creating an elastic beanstalk environment will create a load balanced environment by default, which can be expensive, so I suggest you change the configuration quickly.   You may also wish to play around with what ec2 instances are used etc.

---

### FURTHER WORK

---

This document was intended to be a start project that can be installed at a relatively low cost on AWS Lightsail or AWS Elastic Beanstalk.   I have used these systems because you can avoid the use of Load Balancers, which are expensive and have very little benefit when you creating a test/trial site, however this project has lots of area's that could be improved.   Some of these topics are mentioned below:

###### HTTPS

At present I have not tried https on Lightsail, but it looks relatively easy to install, however HTTPS can be difficult to setup on a Single Instance Elastic Beanstalk environment (it is easy on a Load Balanced environment).   There are ways around this, perhaps including a lightsail loadbalancer.   These links may help:

> https://aws.amazon.com/premiumsupport/knowledge-center/elastic-beanstalk-https-configuration/
> http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-elb.html
> http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/https-singleinstance-python.html
> https://lightsail.aws.amazon.com/ls/docs/en_us/articles/create-lightsail-load-balancer-and-attach-lightsail-instances

###### UNITTESTS AND CODEPIPELINE

This project has been setup to help initiate a development environment and I have excluded any adjustments for code pipeline.   The installation instructions are very manual, but can be setup relatively easily and I think that it provides a good foundation for initiating a project.

A naturaly extension for this is to add a set of unit tests and incorporate the project into code pipeline.   I think this system is brilliant when setup correctly.   You check your project into github or code commit and then the code is extracted, tests are run and then it is deployed into a production/test environment.

https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html

###### ECS AND FARGATE

ECS and FARGATE are very interesting systems for large scale projects, however at present it is not possible to setup an elastic ip address on fargate.   Load balancers are expensive, so I have avoided using this at present.