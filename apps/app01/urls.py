#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from apps.app01 import api,views

 #Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'blogs', api.BLogViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^index/', views.index),
    url(r'^serverinfo/', views.serverinfo),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
