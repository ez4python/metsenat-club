#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn root.wsgi:application --bind 0.0.0.0:8000
