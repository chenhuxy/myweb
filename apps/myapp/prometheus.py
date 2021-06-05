#!/usr/bin/env python
#coding:utf-8
import json
import urllib
from urllib import request,error
import requests
from apps.myapp.login_required import outer
from django.shortcuts import render_to_response
from myweb.settings import PROM_URL,PROM_USER,PROM_PASSWROD


import sys

class PromTools:
    def __init__(self,address,username,password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api/v1/alerts' %self.address
        self.header = {"Content-Type":"text/plain"}

    def alert_get(self):
        try:
            ret = requests.get(self.url,auth=('admin','admin'),timeout=1,)
           # print(json.loads(ret.text))
            result = ret.text
        except Exception as e:
            print ("Error as ",e)
            result = ''
        return result

'''
if __name__ == "__main__":
    for prom_addres in prometheus_addresses:
        address,username,password = prom_addres.split(',')
        p = PromTools(address=address, username=username, password=password)
        content = p.alert_get()
    print    (content)
'''
@outer
def prometheus_alert(request,*args,**kwargs):
    server = PromTools(PROM_URL,PROM_USER,PROM_PASSWROD)
    try:
        msg = json.loads(server.alert_get())
        userDict = request.session.get('is_login', None)
        res = {'msg':msg['data']['alerts'],'login_user': userDict['user'],'count':len(msg['data']['alerts']),}
        print(type(msg['data']['alerts']))
        return render_to_response('monitor/prometheus.html',res)
    except:
        return render_to_response('monitor/500.html')

def prometheus_alert_count(*args,**kwargs):
    try:
        server = PromTools(PROM_URL,PROM_USER,PROM_PASSWROD)
        msg = json.loads(server.alert_get())
        result = len(msg['data']['alerts'])
    except:
        result = None
    return result