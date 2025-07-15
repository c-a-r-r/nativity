#!/bin/sh

echo "Waiting for MySQL to be ready..."
while ! nc -z db 3306; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn server..."
gunicorn crm.wsgi:application --bind 0.0.0.0:8000
