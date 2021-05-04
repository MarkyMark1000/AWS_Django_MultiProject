#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: clean help venv su

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Clean:"
	@echo "make clean	    		- DANGER - remove .py files, venv, coverage etc."
	@echo "Virtual Env:"
	@echo "make venv	    		- Make the virtual environment."
	@echo "Superuser:"
	@echo "make su	    			- Make super user."
	@echo "Build/Run:"
	@echo "make run-local-debug	    	- Run project locally in debug mode"
	@echo "make run-local	    		- Run project locally"
	@echo "make run-dock	    		- Run project using docker"
	@echo "make run-prod	    		- Build production version of docker image"
	@echo "Testing:"
	@echo "make test   			- Run the Test in the virtual environment."
	@echo "make cov-html			- Build HTML coverage report."
	@echo ""

clean:
	@echo ""
	@echo "*** clean ***"
	@echo ""
	(rm -rf venv; rm -rf *.pyc; find . -type d -name  "__pycache__" -exec rm -r {} +; )
	(rm -rf htmlcov; rm -rf .coverag*;)
	(rm -rf .elasticbeanstalk; rm -rf .dockerignore; rm -rf .gitignore;)
	(rm -rf d*.sqlit*; )
	@echo ""

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf venv; python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt; )
	@echo ""

su:
	@echo ""
	@echo "*** create superuser ***"
	@echo ""
	( source venv/bin/activate; python3 manage.py createsuperuser; )
	@echo ""

run-local-debug:
	@echo ""
	@echo "*** run project locally in debug mode ***"
	@echo "  (warning no collection of static)"
	@echo ""
	@echo "   http://localhost:8080"
	@echo "   http://localhost:8080/pscountries/"
	@echo "   http://localhost:8080/brokers/"
	@echo "   http://localhost:8080/monitoredaccounttype/"
	@echo "   http://localhost:8080/symbols/"
	@echo "   http://localhost:8080/marketdata/"
	@echo ""
	( source venv/bin/activate; export DJANGO_DEBUG='True'; export API_ENVIRONMENT='Local'; python3 manage.py collectstatic --noinput; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 8080 --nostatic; )
	@echo ""

run-local:
	@echo ""
	@echo "*** run project locally ***"
	@echo ""
	@echo "   http://localhost:8080"
	@echo "   http://localhost:8080/pscountries/"
	@echo "   http://localhost:8080/brokers/"
	@echo "   http://localhost:8080/monitoredaccounttype/"
	@echo "   http://localhost:8080/symbols/"
	@echo "   http://localhost:8080/marketdata/"
	@echo ""
	( source venv/bin/activate; export DJANGO_DEBUG='False'; export API_ENVIRONMENT='Local'; python3 manage.py collectstatic --noinput; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 8080 --nostatic; )
	@echo ""

run-dock:
	@echo ""
	@echo "*** run project locally on docker ***"
	@echo "  (don't forget to clean up images/containers)"
	@echo ""
	@echo "   http://localhost:8080"
	@echo "   http://localhost:8080/pscountries/"
	@echo "   http://localhost:8080/brokers/"
	@echo "   http://localhost:8080/monitoredaccounttype/"
	@echo "   http://localhost:8080/symbols/"
	@echo "   http://localhost:8080/marketdata/"
	@echo ""
	( docker build --build-arg DJANGO_DEBUG=True --build-arg API_ENVIRONMENT=Docker -t mjw/brokerdata .; docker run -p 8080:8080 mjw/brokerdata; )
	@echo ""

build-dock-prod:
	@echo ""
	@echo "*** build production version of docker (don't run) ***"
	@echo "  (don't forget to clean up images/containers)"
	@echo ""
	@echo ""
	( docker build --build-arg DJANGO_DEBUG=False --build-arg API_ENVIRONMENT=Prod -t mjw/brokerdata .; )
	@echo ""

test:
	@echo ""
	@echo "Running test in venv virtual environment."
	@echo ""
	@echo "   to debug, you could use the --keepdb option"
	@echo ""
	( source venv/bin/activate; export DJANGO_DEBUG='False'; export API_ENVIRONMENT='Local'; python3 manage.py test --noinput; )
	@echo ""

cov-html:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; rm -rf .coverag*; rm -rf htmlcov; sleep 1; export DJANGO_DEBUG='False'; export API_ENVIRONMENT='Local'; coverage run manage.py test --noinput ; coverage html)
	@echo ""