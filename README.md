# Django Backoffice for www.sudu.film 

## Prerequisite 

- Python 3 
- Docker client
- Create or obtain .env.dev and .env.prod ( Not in version control )

## environnement variable

If you can't obtain a .env file from the team. Setup keys as follow for dev : 

```
echo -e 
"DEBUG=1 \n
SECRET_KEY=foo \n
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \n
SQL_ENGINE=django.db.backends.postgresql \n
SQL_DATABASE=sudu_django_dev \n
SQL_USER=sudu_django \n
SQL_PASSWORD=sudu_django \n
SQL_HOST=db \n
SQL_PORT=5432 \n
DATABASE=postgres \n

DJANGO_SU_NAME=admin \n
DJANGO_SU_EMAIL=contact@noreply.com \n
DJANGO_SU_PASSWORD=unsecure \n"
> .env.dev
```

## install steps ( locally build docker image )

```
$ git clone git@github.com:antoineclaval/sudu_django.git
$ cd sudu_django
$ python3.x -m venv env
$ source env/bin/activate
```
Be sure to have a sudu_django/.env.dev file created at this point. Then run:

```
$ set -a; source .env.dev; set +a
$ docker-compose up -d --build
```

After the last step, running ```docker ps``` should give you two running containers: ```sudu_django_web``` and ```postgres:12.0-alpine```
You can also access : http://localhost:8000/ and http://localhost:8000/admin
Default admin creds : admin/unsecure

## Interact with the docker image

- The django process will restart the server and rebuild it at filechange.
- Exec arbitrary commands on container "web" from compose file : ```docker-compose exec web echo "LALALA" ```
- See running logs : ```docker logs -f <ContainerID>```
- Better see running logs : ```docker logs -f `docker ps -qf name=sudu_django_web` ```
- Stop everything, keep the data : ```docker-compose down```
- Stop everything and delete the volumes : ```docker-compose down -v```
- Interative sh script session : ``docker exec -it <ContainerID> /bin/sh ``

#### Django specific docker interaction 

- prepare DB  migration ```$ docker-compose exec web python manage.py makemigrations```
- apply migration ```$ docker-compose exec web python manage.py migrate --noinput```
- django shell ```docker-compose exec web python manage.py shell```
- django create super user ```docker-compose exec web python manage.py createsuperuser``` 

## Interact with the PostGres Instance

Check that the 5432 port is mapped to the localmachine ( ```0.0.0.0:5432->5432/tcp``` in ```docker ps``` )

- psql -h localhost -p 5432 -U sudu_django -d sudu_django_dev -W
- \dt ( show tables ) 

## DB backup / restore 

- Backup ```docker exec <containerID> pg_dump -U sudu_django sudu_django_dev > backup.sql```
- Restore ```docker exec -i <containerID> psql -U sudu_django -d sudu_django_dev < backup.sql```

## Docker for prod
```
$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

## Docker schenanigans 

- get ID of running container. ```docker ps -qf name=sudu_django_web```
- basic disk-usage ```docker system df -v```
- See : build-docker.sh


### Notes : originals generation steps 

```
$ mkdir sudu_django
$ cd sudu_django
$ python3.8 -m venv env
$ source env/bin/activate
(env)$ pip install django==2.2.6
(env)$ django-admin.py startproject sudu_django .
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
- See : https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

