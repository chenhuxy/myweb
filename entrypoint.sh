#!/usr/bin/env sh


python3 manage.py runserver 0.0.0.0:8000 &
python3 -m celery worker -A myweb -P eventlet -l info -f /myweb/logs/celery.log
