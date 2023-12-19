#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py makemigrations
python manage.py migrate
python manage.py ensure_superuser

python manage.py runserver 0.0.0.0:8000