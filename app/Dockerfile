FROM python:3.13-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies for psycopg, Pillow, lxml
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libc-dev libxslt-dev \
    && apk add postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk add libxslt libpq

# Copy dependency file and install
COPY ./pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# Delete virtual build deps
RUN apk del build-deps

# Copy entrypoint
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# Copy project
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
