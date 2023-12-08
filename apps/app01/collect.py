#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import salt.client
import json
import time
import os
import httplib
import urllib


# import http.client
# import urllib.parse

def RequestUrl(host, port, source, params, timeout):
    headers = {'Content-Type': 'application/json;charset=utf-8', }
    try:
        conn = httplib.HTTPConnection(host, port, timeout)
        # conn = http.client.HTTPConnection(host,port,timeout)
        conn.request('POST', source, params, headers)
        response = conn.getresponse()
        original = response.read()
        # print(original)
    except Exception as e:
        raise e
    return original


def server_info():
    try:
        client = salt.client.LocalClient()
        target = '*'
        grains = client.cmd(target, "grains.items")
        disks = client.cmd(target, "disk.usage")
        serverinfos = []
        for i in grains.keys():
            serverinfo = {}
            hostname = grains[i]["nodename"]
            OS = grains[i]["os"] + " " + grains[i]["osrelease"]
            virtual = grains[i]["virtual"]
            manufacturer = grains[i]["manufacturer"]
            serialnumber = grains[i]["serialnumber"]
            model = grains[i]["productname"]
            biosinfo = {}
            meminfo = {}
            cpuinfo = {}
            diskinfo = {}
            nicinfo = {}
            biosinfo["version"] = grains[i]["biosversion"]
            biosinfo["releasedate"] = grains[i]["biosreleasedate"]
            div = divmod(grains[i]["mem_total"], 1024)
            w = 2
            if div[1] == 0:
                meminfo["mem_total"] = str(round(div[0], w)) + "G"
            meminfo["mem_total"] = str(round(div[0] + div[1] / 1024.0, w)) + "G"
            cpuinfo["num_cpus"] = grains[i]["num_cpus"]
            cpuinfo["model"] = grains[i]["cpu_model"]
            # grains[i]["hwaddr_interfaces"].pop("lo")
            diskinfo["disks"] = grains[i]["disks"]
            diskinfo["capacity /"] = str(round(float(disks[i]["/"]["1K-blocks"]) / 1048576, w)) + "G"
            diskinfo["capacity /boot"] = str(round(float(disks[i]["/boot"]["1K-blocks"]) / 1048576, w)) + "G"
            nicinfo["interfaces"] = grains[i]["hwaddr_interfaces"]
            nicinfo["ipv4"] = grains[i]["ip4_interfaces"]
            serverinfo["hostname"] = hostname
            serverinfo["OS"] = OS
            serverinfo["virtual"] = virtual
            serverinfo["manufacturer"] = manufacturer
            serverinfo["serialnumber"] = serialnumber
            serverinfo["model"] = model
            serverinfo["biosinfo"] = biosinfo
            serverinfo["meminfo"] = meminfo
            serverinfo["cpuinfo"] = cpuinfo
            serverinfo["diskinfo"] = diskinfo
            serverinfo["nicinfo"] = nicinfo
            # serverinfo["status"] = True
            timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            serverinfo_json = json.dumps(serverinfo)
            paths = '/' + 'root' + '/' + 'report' + '/' + i + '/' + timestamp
            if not os.path.exists(paths):
                os.makedirs(paths)
            filename = paths + '/' + 'info.json'
            with open(filename, "w") as f:
                # with open (filename,"a+" ) as f:
                # if os.path.getsize(filename) == 0:
                # msg = timestamp+" "+serverinfo_json
                msg = serverinfo_json
                # else:
                # msg = "\n"+timestamp+" "+serverinfo_json
                f.write(msg)
            serverinfos.append(serverinfo, )
            # print(serverinfos)
        return serverinfos
    except Exception as e:
        print("error:", e)


if __name__ == '__main__':
    data = server_info()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # count = 1
    if data:
        # while True:
        for i in data:
            # print(i)
            RequestData = json.dumps({'data_json': i})
            params = json.dumps(urllib.urlencode({'data_encode': i}))
            result = RequestUrl('192.168.0.103', '8000', '/api/serverinfo/', params, 30)
            # print('--------第%d次请求，结果为:%s-------'%(count,result))
            print('%s %s msg:%s' % (timestamp, i["hostname"], result))
            # params = json.dumps(urllib.parse.urlencode({'data_encode':server_info()}))
            # print(RequestData)
            # print(params)
        # count += 1
        # time.sleep(5)
