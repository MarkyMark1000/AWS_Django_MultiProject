#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: clean help venv

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Clean:"
	@echo "make clean	    		- DANGER - remove .py files, venv, coverage etc."
	@echo "Virtual Env:"
	@echo "make venv	    		- Make the virtual environment."
	@echo "Run:"
	@echo "make run-local-debug	    	- Run project locally in debug mode"
	@echo "make run-local	    		- Run project locally"
	@echo "make run-dock	    		- Run project using docker"
	@echo "Testing:"
	@echo "make test   			- Run the Test in the virtual environment."
	@echo "make cov-html			- Build HTML coverage report."
	@echo ""

clean:
	@echo ""
	@echo "*** clean ***"
	@echo ""
	(rm -rf venv; rm -rf *.pyc; find . -type d -name  "__pycache__" -exec rm -r {} +; )
	(rm -rf htmlcov; rm -rf .coverage;)
	(rm -rf .elasticbeanstalk; rm -rf .dockerignore; rm -rf .gitignore;)
	(rm -rf d*.sqlit*; )
	@echo ""

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf venv; python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt; )
	@echo ""

run-local-debug:
	@echo ""
	@echo "*** run project locally in debug mode ***"
	@echo "  (warning no collection of static)"
	@echo ""
	@echo "   http://localhost:8080"
	@echo ""
	( source venv/bin/activate; export DJANGO_DEBUG='True'; python3 manage.py collectstatic --noinput; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 8080 --nostatic; )
	@echo ""

run-local:
	@echo ""
	@echo "*** run project locally ***"
	@echo ""
	@echo "   http://localhost:8080"
	@echo ""
	( source venv/bin/activate; export DJANGO_DEBUG='False'; python3 manage.py collectstatic --noinput; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 8080 --nostatic; )
	@echo ""

run-dock:
	@echo ""
	@echo "*** run project locally on docker ***"
	@echo "  (don't forget to clean up images/containers)"
	@echo ""
	@echo "   http://localhost:8080"
	@echo ""
	( docker build -t mjw/basiclogin .; docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/basiclogin; )
	@echo ""

test:
	@echo ""
	@echo "Running test in venv virtual environment."
	@echo ""
	@echo "   to debug, you could use the --keepdb option"
	@echo ""
	( source venv/bin/activate; python3 manage.py test --noinput; )
	@echo ""

cov-html:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; rm -rf .coverag*; rm -rf htmlcov; sleep 1; coverage run manage.py test --noinput ; coverage html)
	@echo ""