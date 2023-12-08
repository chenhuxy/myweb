#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from apps.app01 import models
# from rest_framework.decorators import detail_route, list_route
from rest_framework import response
from django.shortcuts import HttpResponse


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Serializers define the API representation.
class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Blog
        depth = 1
        fields = ('url', 'title', 'content',)


# ViewSets define the view behavior.
class BLogViewSet(viewsets.ModelViewSet):
    queryset = models.Blog.objects.all()
    serializer_class = BlogSerializer

    # @list_route()
    def detail(self, request):
        print(request)
        # return HttpResponse('ok')
        return response.Response('ok')
