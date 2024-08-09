#!/bin/sh
echo "EntryPoint Shell Scripts Started !"

if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for postgres..."

    until nc -z $DB_HOST $DB_PORT; do
      echo "Postgres is unavailable - sleeping"
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
