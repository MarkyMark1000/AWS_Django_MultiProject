# OVERVIEW

This is one big project that contains multiple seperate little projects within it.   Each directory should be a project in its own right and you should be able to install it onto AWS using Lightsail or Elastic Beanstalk.   I have not concentrated on Fargate because at the time, the IP address could not be made elastic and I found the use of load balancers expensive.   I also have not incorporated any CodePipeline adjustments.

It is my intention not to worry too much about security.   I do not cover setting up HTTPS here and I would normally hide things such as database passwords within the parameter store.   This will not be done in these projects.

As this code is public and I make adjustments to it on an ad-hoc basis, there is a risk that it may become out of date or that I may not have completely finished a project before it is added to github.

These projects will largely use Docker containers, on AWS, so I will be making extensive use of Docker, the AWS CLI, EB and LightSail features.   Please see the following links for the appropriate method to install these sytems:

> https://docs.docker.com/get-docker/

> https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

> https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html

> https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-install-software

### .gitignore

---

This is just a warning.   There is a .gitignore file within the AWS_Django_MultiProject directory, which is important.   Some of the sub projects create extra .gitignore files that are local to the project when elastic beanstalk is setup.   These local versions of the .gitignore files are less important and can be deleted.

With respect to the main .gitignore file, this file excludes some very specific files which are used to save security credentials, such as ses_account.py.   Please see the README.md files in the projects such as 1_SendEmailFromWebsite.py for more information on this.