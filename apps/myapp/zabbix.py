#!/usr/bin/env python
# coding:utf-8
import json
import urllib
from urllib import request, error
import requests
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from django.shortcuts import render_to_response
from myweb.settings import ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD

import sys


class ZabbixTools:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api_jsonrpc.php' % self.address
        self.header = {"Content-Type": "application/json-rpc"}

    def user_login(self):
        data = {"jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.username,
                    "password": self.password},
                "id": 0,
                }
        # request = urllib.request.Request(self.url,data=data,headers=self.header)
        try:
            ret = requests.post(self.url, data=json.dumps(data), headers=self.header, timeout=1, )
            print(json.loads(ret.text)['result'])
            result = json.loads(ret.text)['result']
        except Exception as e:
            print("Auth Failed, please Check your name and password:", e)
            result = None
        return result

    def trigger_get(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "triggerid",
                    "description",
                    "priority"
                ],
                "filter": {
                    "value": 1
                },
                "sortfield": "priority",
                "sortorder": "DESC",
                "min_severity": 4,
                "skipDependent": 1,
                "monitored": 1,
                "active": 1,
                "expandDescription": 1,
                "selectHosts": ['host'],
                "selectGroups": ['name'],
                "only_true": 1
            },
            "auth": self.user_login(),
            "id": 1
        }
        # request = urllib.request.Request(self.url,data=data,headers=self.header)
        try:
            ret = requests.post(self.url, data=json.dumps(data), headers=self.header, timeout=1, )
            # print(json.loads(ret.text))
            result = json.loads(ret.text)
        except Exception as e:
            print("Error as ", e)
            result = None
        return result


'''
if __name__ == "__main__":
    for zabbix_addres in zabbix_addresses:
        address,username,password = zabbix_addres.split(',')
        z = ZabbixTools(address=address, username=username, password=password)
        content = z.trigger_get()
    print    (content)
'''


@custom_login_required
@custom_permission_required('myapp.view_monitor')
def zabbix_trigger(request, *args, **kwargs):
    server = ZabbixTools(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD)
    msg = server.trigger_get()
    # lst_k = list(msg)
    # lst_v = [msg.values()]
    # print(lst_v[0])
    # for k,v in msg.items():
    #     print(k,v)
    # print(type(msg))
    userDict = request.session.get('is_login', None)
    try:
        res = {'msg': msg['result'], 'login_user': userDict['user'], 'count': len(msg['result']), }
        print(type(msg['result']), len(msg['result']))
        return render_to_response('monitor/zabbix.html', res)
    except:
        return render_to_response('500.html', res, status=500)


def zabbix_alert_count(*args, **kwargs):
    try:
        server = ZabbixTools(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD)
        msg = server.trigger_get()
        result = len(msg['result'])
    except:
        result = None
    return result
