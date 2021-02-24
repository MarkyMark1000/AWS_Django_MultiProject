#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: clean help

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Clean:"
	@echo "make clean	    		- Remove .py files, venv, coverage etc."
	@echo "Virtual Env:"
	@echo "make venv	    		- Make the virtual environment."
	@echo "Run:"
	@echo "make run-local	    		- Run project locally"
	@echo "make run-dock	    		- Run project using docker"

clean:
	@echo ""
	@echo "*** clean ***"
	@echo ""
	(rm -rf venv; rm -rf *.pyc; rm -rf *_pycache_*; )
	(rm -rf htmlcov; rm -rf .coverage;)
	(rm -rf .elasticbeanstalk; rm -rf .dockerignore; rm -rf .gitignore;)
	(rm -rf db.sqlite3; )
	@echo ""

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf venv; python3 -m venv venv; source venv/bin/activate; pip3 install -m requirements.txt; )
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
	( docker build -t mjw/sendemail .; docker run -e DJANGO_DEBUG='False' -p 8080:8080 mjw/sendemail; )
	@echo ""