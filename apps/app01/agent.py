#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time, json, http.client, urllib
import urllib.parse

server_info = {
    "cpu": "8core,E5",
    "mem": "128GB",
    "disk": "1T",
    "nic": "10000bpsX2",
}


def RequestUrl(host, port, source, params, timeout):
    headers = {'Content-Type': 'application/json;charset=utf-8', }
    try:
        # conn = httplib.HTTPConnection(host,port,timeout)
        conn = http.client.HTTPConnection(host, port, timeout)
        conn.request('POST', source, params, headers)
        response = conn.getresponse()
        original = response.read()
        # print(original)
    except Exception as e:
        raise e
    return original


if __name__ == '__main__':
    count = 0
    while True:
        RequestData = json.dumps({'data_json': server_info})
        params = json.dumps(urllib.parse.urlencode({'data_encode': server_info}))
        print(params)
        print(RequestData)
        result = RequestUrl('127.0.0.1', '8000', '/api/serverinfo/', params, 30)
        print('--------第%d次请求，结果为:%s-------' % (count, result))
        count += 1
        time.sleep(3)
