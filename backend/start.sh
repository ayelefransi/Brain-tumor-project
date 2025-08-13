#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn tumorDetection.wsgi:application --bind 0.0.0.0:9000 --workers ${GUNICORN_WORKERS:-3}