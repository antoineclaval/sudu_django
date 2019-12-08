# Django Backoffice for www.sudu.film 

## Install steps 

### Prerequisite 

- Python 3 
- Docker client

###

$ git clone git@github.com:antoineclaval/sudu_django.git
$ python -m venv env
$ source env/bin/activate
$ cd app
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ docker-compose exec web python manage.py migrate --noinput

#### Notes : originals generation steps 

$ mkdir sudu_django
$ cd sudu_django
$ python3.8 -m venv env
$ source env/bin/activate
(env)$ pip install django==2.2.6
(env)$ django-admin.py startproject sudu_django .
(env)$ python manage.py migrate
(env)$ python manage.py runserver

- See : https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
