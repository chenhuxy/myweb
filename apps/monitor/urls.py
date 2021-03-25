#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.monitor import views

urlpatterns = [


    url(r'',views.get_host),
    url(r'^details/(\d+)', views.get_host_detail, name='get_host_detail'),


]
