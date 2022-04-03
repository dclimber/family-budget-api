FROM python:3.8.12-slim-buster

ARG USER_ID
ARG USER_NAME

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat \
    gettext \
    postgresql-client-11 \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --uid $USER_ID --user-group --create-home $USER_NAME

ENV APP_HOME=/home/$USER_NAME/djangoapp

RUN mkdir -p $APP_HOME/static \
    && mkdir $APP_HOME/media \
    && mkdir $APP_HOME/logs \
    && mkdir $APP_HOME/backups

WORKDIR $APP_HOME/src

RUN python -m venv ../env

COPY requirements.txt .

RUN $APP_HOME/env/bin/pip install -U pip \
    && $APP_HOME/env/bin/pip install -r requirements.txt

RUN chown -R $USER_ID:$USER_ID $APP_HOME

COPY --chown=$USER_ID:$USER_ID . .

RUN chmod +x $APP_HOME/src/scripts/django_entrypoint.sh

USER $USER_ID
