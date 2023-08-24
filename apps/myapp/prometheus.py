#!/usr/bin/env python
#coding:utf-8
import json
import urllib
from urllib import request,error
import requests
from apps.myapp.auth_helper import custom_login_required,custom_permission_required
from django.shortcuts import render_to_response
from myweb.settings import PROM_URL,PROM_USER,PROM_PASSWROD
from apps.myapp import common
from apps.myapp import page_helper

import sys

class PromTools:
    def __init__(self,address,username,password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api/v1/alerts' % self.address
        self.header = {"Content-Type":"text/plain"}

    def alert_get(self):
        try:
            ret = requests.get(self.url,auth=(self.username, self.password), timeout=5,)
            print(json.loads(ret.text))
            result = ret.text
        except Exception as e:
            print ("Error as ",e)
            result = ' '
        return result

'''
if __name__ == "__main__":
    for prom_addres in prometheus_addresses:
        address,username,password = prom_addres.split(',')
        p = PromTools(address=address, username=username, password=password)
        content = p.alert_get()
    print    (content)
'''
@custom_login_required
@custom_permission_required('myapp.view_monitor')
def prometheus_alert(request,*args,**kwargs):
    server = PromTools(PROM_URL,PROM_USER,PROM_PASSWROD)
    try:
        alerts = json.loads(server.alert_get())['data']['alerts']
        count = len(alerts)
        page = common.try_int(kwargs['page'], 1)
        perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
        pageinfo = page_helper.pageinfo(page, count, perItem)
        alerts= alerts[pageinfo.start:pageinfo.end]
        page_string = page_helper.pager_prometheus_alert_list(request, page, pageinfo.pageCount)
        userDict = request.session.get('is_login', None)
        msg = {'alerts': alerts, 'count': count, 'pageCount': pageinfo.pageCount,
               'page': page_string, 'login_user': userDict['user'], }
        return render_to_response('monitor/prometheus.html',msg)
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