#!/usr/bin/env sh

python3 manage.py makemigrations && python3 manage.py migrate
python3 -m celery worker -A myweb -P eventlet -l info &
python3 manage.py runserver 0.0.0.0:8000
