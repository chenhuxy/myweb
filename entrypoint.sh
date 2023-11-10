#!/usr/bin/env sh

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000 &
# python3 -m celery worker -A myweb -P eventlet -l info -f /myweb/logs/celery.log
# 启动多个worker,建议cpu核数
python3 -m celery worker -A myweb -P solo -n worker1 -l info -f /myweb/logs/celery.log &
python3 -m celery worker -A myweb -P solo -n worker2 -l info -f /myweb/logs/celery.log &
python3 -m celery worker -A myweb -P solo -n worker3 -l info -f /myweb/logs/celery.log &
python3 -m celery worker -A myweb -P solo -n worker4 -l info -f /myweb/logs/celery.log
