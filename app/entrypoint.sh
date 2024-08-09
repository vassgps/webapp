#!/bin/sh
echo "EntryPoint Shell Scripts Started !"

if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
