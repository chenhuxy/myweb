#!/usr/bin/env python
#coding:utf-8
import json
import urllib
from urllib import request,error
import requests
from apps.myapp.login_required import outer
from django.shortcuts import render_to_response


import sys
#prometheus_addresses=['http://10.181.1.13/prometheus,admin,admin']
class PromTools:
    def __init__(self,address,username,password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api/v1/alerts' %self.address
        self.header = {"Content-Type":"text/plain"}

    def alert_get(self):
        try:
            ret = requests.get(self.url,auth=('admin','admin'))
           # print(json.loads(ret.text))
        except Exception as e:
            print ("Error as ",e)
        return ret.text

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
    address = 'http://10.181.1.13/prometheus'
    username = 'admin'
    password = 'admin'
    server = PromTools(address,username,password)
    msg = json.loads(server.alert_get())
    userDict = request.session.get('is_login', None)
    res = {'msg':msg['data']['alerts'],'login_user': userDict['user'],'count':len(msg['data']['alerts']),}
    print(type(msg['data']['alerts']))
    return render_to_response('monitor/prometheus.html',res)

def prometheus_alert_count(*args,**kwargs):
    address = 'http://10.181.1.13/prometheus'
    username = 'admin'
    password = 'admin'
    server = PromTools(address, username, password)
    msg = json.loads(server.alert_get())
    return len(msg['data']['alerts'])