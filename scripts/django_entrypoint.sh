#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ "$POSTGRES_USER" = "postgres" ]; then
    echo "Waiting for PostgreSQL to become available..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL is available"
fi

echo "Making migrations."
$APP_HOME/env/bin/python manage.py migrate --noinput

echo "Collecting static files."
$APP_HOME/env/bin/python manage.py collectstatic --noinput

echo "Loading fixtures."
$APP_HOME/env/bin/python manage.py loaddata fixtures/fixtures.json

echo "Starting gunicorn."
$APP_HOME/env/bin/gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

exec "$@"
