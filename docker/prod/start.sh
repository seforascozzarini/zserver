#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py ensure_superuser

gunicorn app.wsgi:application --bind 0.0.0.0:8000