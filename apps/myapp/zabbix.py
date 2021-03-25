#!/usr/bin/env python
#coding:utf-8
import json
import urllib
from urllib import request,error
import requests
from apps.myapp.login_required import outer
from django.shortcuts import render_to_response


import sys
#zabbix_addresses=['http://10.180.10.84/zabbix,hu.chen,Qoros0507']
class ZabbixTools:
    def __init__(self,address,username,password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api_jsonrpc.php' %self.address
        self.header = {"Content-Type":"application/json-rpc"}

    def user_login(self):
        data = { "jsonrpc": "2.0",
                 "method": "user.login",
                 "params": {
                            "user": self.username,
                            "password": self.password},
                            "id": 0,
                }
       # request = urllib.request.Request(self.url,data=data,headers=self.header)
        try:
            ret = requests.post(self.url, data=json.dumps(data), headers=self.header)
            print(json.loads(ret.text)['result'])
        except Exception as e:
            print ("Auth Failed, please Check your name and password:",e)
        return json.loads(ret.text)['result']

    def trigger_get(self):
        data = {
                   "jsonrpc":"2.0",
                   "method":"trigger.get",
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
                   "id":1
        }
       # request = urllib.request.Request(self.url,data=data,headers=self.header)
        try:
            ret = requests.post(self.url, data=json.dumps(data), headers=self.header)
           # print(json.loads(ret.text))
        except Exception as e:
            print ("Error as ",e)
        return json.loads(ret.text)
'''
if __name__ == "__main__":
    for zabbix_addres in zabbix_addresses:
        address,username,password = zabbix_addres.split(',')
        z = ZabbixTools(address=address, username=username, password=password)
        content = z.trigger_get()
    print    (content)
'''

@outer
def zabbix_trigger(request,*args,**kwargs):
    address = 'http://10.180.10.84/zabbix'
    username = 'hu.chen'
    password = 'Qoros0507'
    server = ZabbixTools(address,username,password)
    msg= server.trigger_get()
   # lst_k = list(msg)
   # lst_v = [msg.values()]
   # print(lst_v[0])
   # for k,v in msg.items():
   #     print(k,v)
   # print(type(msg))
    userDict = request.session.get('is_login', None)
    res= {'msg':msg['result'],'login_user': userDict['user'],'count':len(msg['result']),}
    print(type(msg['result']),len(msg['result']))
    return render_to_response('monitor/zabbix.html',res)