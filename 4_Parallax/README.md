# OVERVIEW

Previously, I worked on a project that used parallax scrolling using "background-attachment: fixed".   Unfortunately I found that I had to turn the effect off when viewing the page on an iPhone because it didn't work properly.

Initially, I did not have time to investigate this furthur, but I have noticed that some websites do manage to get this to work and I wanted a template should I need to use it in the future.

The first page demonstrates the use of "background-attachment: fixed" and it probably won't work on an iPhone.

The second page is taken from Keith Clark's page (see Relevant Links at the bottom).   I suggest taking a look at this website.   It is very interesting, especially the debug section where you can see the different layers of the site.

The third page demonstrates how I have used this technique to move multiple images and a foreground with a parallax effect that work's on an iPhone.   Some work could be done to blend the pictures in more and add a footer, but the basic concept is present.

I have tested this with an iPhone, Safari, Chrome, Opera and Edge on my local computer and it appears to work effectively.   Unfortunately I do not have access to extensive browser
testing software, but I suspect that this is unlikely to work on older browsers.   I have
used Bootstrap 4 here!

### Make File

---

The settings.py file has been adjusted to display the ip/port on on the local network and
the make file has been adjusted to use 0.0.0.0:8080.   This should make the site accessible
on the local network so that it can be viewed on an iPhone.   It is extremely unlikely that
this feature will work properly if it is run using Docker.

This has not been tested on a live site.

### MAKEFILE

---

A makefile has been created to help simplify the running of repetitive commands.   It can be used to clean the environment, create a new virtual environment, run the code locally and run the code within Docker.:

> make

> make help

You may need to regularly clean up docker images and containers if you use this extensively.   The makefile does not currently install or deploy this project to Lightsail or Elastic Beanstalk.

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
docker build -t mjw/parallax .
```

3 - You should then have a docker image, you can have a look at these using the following command:

```
docker images
```

4 - Run the docker image:

```bash
docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/parallax
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

### INSTALLATION ONTO LIGHTSAIL

---

###### WARNING

---

If you deploy this onto Elastic Beanstalk, it can be very easy to
use an instance size (eg t2.nano) that is small and may not have
enough memory.   To check the memory, ssh into and EC2 instance
and consider running some of the following:

```
sudo su -
free -m
cat /proc/meminfo
vmstat -s
docker ps -a
docker logs -f <Container ID>
docker stats
```

###### OVERVIEW

---

First, create a lightsail container project.   I would recommend using a Micro with a scale of 1 to ensure the costs are at a minimum to start with.

Do not setup a deployment yet, but call your service something like this:

> django-parallax

We are going to set this up using 'My Local Machine' and there are some advanced instructions on lightsail about how to do this.

Get the domain from lightsail and update the ALLOWED_HOSTS in the settings.py file of the parallax project.   It should look something like this:

> "django-parallax.6hbnjaadkuqb2.eu-west-1.cs.amazonlightsail.com"

You need to create a docker image and test it as mentioned previously.

```
docker build -t mjw/parallax .
```
```  
docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/parallax
```
(*DJANGO_DEBUG may not be relevant and is dependent upon how the Dockerfile is setup.*)

Use the following command to get the REPOSITORY and TAG for the docker image that you just created:

```
docker images
```

Now run the aws command line to push the docker image onto lightsail.   The command should look something like this:

```
aws lightsail push-container-image --region eu-west-1 --service-name django-parallax --label parallax --image mjw/parallax:latest
```
(*mjw/parallax and latest were the REPOSITORY and TAG*)

You should now have an image available on lightsail if you refresh the screen and it will have a name similar to the following:

> ":django-parallax.parallax.4"

Within lightsail, goto 'Deployments' and then 'Create your first deployment'.

Give the container a name, eg:

> "cont-parallax"

and under the image, set the new image that has been sent to lightsail, eg:

> ":django-parallax.parallax.4"

Lightsail containers may not accept environment variables.   Depending upon the setup of your docker file, you may want to add the following:

> DJANGO_DEBUG => False

Also, add an open port of 8080 to HTTP.

Within your public endpoint, select your container name from the combo box, eg:

> "cont-parallax"

Hit save and deploy and then wait for it to finish deploying.

Once it has finished deploying, you should be able to follow your public domain link from lightsail and see the website working on the other end.

---

### INSTALLATION ONTO ELASTIC BEANSTALK

---

###### WARNING

---

If you deploy this onto Elastic Beanstalk, it can be very easy to
use an instance size (eg t2.nano) that is small and may not have
enough memory.   To check the memory, ssh into and EC2 instance
and consider running some of the following:

```
sudo su -
free -m
cat /proc/meminfo
vmstat -s
docker ps -a
docker logs -f <Container ID>
docker stats
```

You will also probably want to Enable 'stickiness' for this application.   It has not been tested extensively on a load balanced environment, but you could look at the Elastic Beanstalk configuration -> Load Balancer.   More information on stickiness can be found here:

> https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-alb.html

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
eb init -i -p docker contParallaxApp
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
eb create contparallax-env
```

```
eb deploy
```

If you have created the environment for the first time, you will need to update the LOCAL_HOSTS in the settings.py file of the parallax project with the appropriate domain from the elastic beanstalk environment, eg:

> "contparallax-env.eba-kihs3gqn.eu-west-1.elasticbeanstalk.com"

Within the .ebextensions directory, there is a file called environment.config.   This file initiates the DJANGO_DEBUG variable, so you may want to change this value depending on if you want to initiate the project in debug or production mode.

If necessary, redeploy using the following command:

```
eb deploy
```

You can now open the website from Elastic Beanstalk, or use the following command:

```
eb open
```

This method of creating an elastic beanstalk environment will create a load balanced environment by default, which can be expensive, so I suggest you change the configuration quickly.   You may also wish to play around with what ec2 instances are used.   Alternatively you could make some adjustements to the .ebextensions directory to force a particular type of environment to be created.

---

### Relevant Links

---

https://stackoverflow.com/questions/24057655/parallax-scrolling-in-safari-on-ios

https://keithclark.co.uk/articles/pure-css-parallax-websites/

This is excellent, try the debug button:  
https://keithclark.co.uk/articles/pure-css-parallax-websites/demo3/
