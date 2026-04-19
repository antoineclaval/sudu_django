# Django Backoffice for www.sudu.film 

## Prerequisites

### System packages

**Fedora:**
```bash
sudo dnf install python3.13 podman podman-compose postgresql libpq-devel libjpeg-devel zlib-devel libxslt-devel gcc
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.13 podman podman-compose postgresql-client libpq-dev libjpeg-dev zlib1g-dev libxslt1-dev gcc
```

**UV** (Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Environment file

Create or obtain `.env.dev` (not in version control). If you can't obtain one from the team:

```bash
cat > .env.dev << 'EOF'
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=sudu_django_dev
SQL_USER=sudu_django
SQL_PASSWORD=sudu_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DJANGO_SU_NAME=admin
DJANGO_SU_EMAIL=contact@noreply.com
DJANGO_SU_PASSWORD=unsecure
EOF
```

## First run (containers)

```bash
git clone git@github.com:antoineclaval/sudu_django.git
cd sudu_django
set -a; source .env.dev; set +a
podman compose up -d --build
podman compose exec web python manage.py migrate --noinput
podman compose exec web python manage.py createsuperuser
```

Access http://localhost:8000/admin

## First run (local, without containers)

Start only PostgreSQL from the compose file (isolated per project, data in a named volume):

```bash
podman compose up -d db
```

Then install and run Django locally:

```bash
cd app
uv sync                        # creates .venv/ and installs all deps
source .venv/bin/activate
set -a; source ../.env.local; set +a
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`.env.local` is identical to `.env.dev` but uses `SQL_HOST=localhost` instead of `db` (the container network name).

Access http://localhost:8000/admin

## Interact with the containers

- The django process will restart the server and rebuild it at filechange.
- Exec arbitrary commands on container "web": ```podman compose exec web echo "LALALA" ```
- See running logs: ```podman logs -f <ContainerID>```
- Stop everything, keep the data: ```podman compose down```
- Stop everything and delete the volumes: ```podman compose down -v```
- Interactive shell session: ```podman exec -it <ContainerID> /bin/sh```

#### Django management commands

- prepare DB migration: ```podman compose exec web python manage.py makemigrations```
- apply migration: ```podman compose exec web python manage.py migrate --noinput```
- django shell: ```podman compose exec web python manage.py shell```
- create super user: ```podman compose exec web python manage.py createsuperuser``` 

## Interact with the PostgreSQL Instance

Check that the 5432 port is mapped to the localmachine ( ```0.0.0.0:5432->5432/tcp``` in ```podman ps``` )

- psql -h localhost -p 5432 -U sudu_django -d sudu_django_dev -W
- \dt ( show tables ) 

## DB backup / restore 

- Backup: ```podman exec <containerID> pg_dump -U sudu_django sudu_django_dev > backup.sql```
- Restore: ```podman exec -i <containerID> psql -U sudu_django -d sudu_django_dev < backup.sql```

## Production deployment

```bash
podman compose -f docker-compose.prod.yml up -d --build
podman compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

## Dependencies

Dependencies are managed via UV with `app/pyproject.toml`. Run `uv sync` in `app/` to install. No requirements.txt.

## Podman Notes

- Always use `podman compose`, not `docker-compose`
- Container images must use full registry paths in compose files (e.g., `docker.io/postgres:16-alpine`) — Podman enforces short-name resolution and will fail without a TTY to prompt
- Bind-mount volumes use `:Z` suffix for SELinux on Fedora (already set in `docker-compose.yml`)
- `podman compose` commands must be run from the project root (where `docker-compose.yml` lives)

## Stack

- Python 3.13 / Django 5.2 LTS
- PostgreSQL 16
- Gunicorn (prod) / runserver_plus (dev)
- Nginx reverse proxy (prod)
- UV package manager
- Podman (rootless)
