#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path
from apps.myapp import consumers

websocket_urlpatterns=[
    path('cmdb/index/deploy/task/get_task_log/', consumers.TasklogConsumer),

]