#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from blog import views

urlpatterns=[
path('',views.get_blogs),
url(r'^detail/(?P<blog_id>\d*)',views.get_details,name="blog_get_detail"),
]

