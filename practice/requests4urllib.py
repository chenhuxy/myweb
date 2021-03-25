#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests

payload = {'user':'elastic','password':'noohle0502'}
ret = requests.get('http://192.168.1.75:9200/',params=payload)
print(ret.url)
print(ret.text)
#print(ret.content)