# OVERVIEW

This is a project that can be installed on AWS Lightsail or AWS Elastic Beanstalk.   When setup you should be able to enter an email address in a field and then an email will be sent to that address.

## TEST DJANGO LOCALLY

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