#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# Create your views here.

from django.shortcuts import render, render_to_response, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import urllib
import urllib.parse


# Create your views here.


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def index(request):
    print(request.method)
    print(request.data)
    return Response([{'asset': '1', 'request_hostname': 'c1.puppet.com'}])


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def serverinfo(request):
    print(request.POST)
    print(request.method)
    if request.method == 'POST':
        print(urllib.parse.unquote(request.data))
        print(request.data)
    return Response('receive ok!')
