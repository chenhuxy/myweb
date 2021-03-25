#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# coding=utf-8
import salt.client as sc
import MySQLdb

db = MySQLdb.connect("192.168.62.200", "root", "kbsonlong", "test")
cur = db.cursor()
# cur.execute('truncate table hostinfo')   #清空主机信息表，当主机较多时慎重处理

###salt调用
local = sc.LocalClient()
###目标主机指定
tgt = "*"

###获取grains，disk信息
grains = local.cmd(tgt, "grains.items")
diskusage = local.cmd(tgt, "disk.usage")

cols = "主机,IP,内存(GB),CPU型号,CPU核数,操作系统 ,/容量(GB),/(使用率）,/data容量(GB),/data(使用率）,/data1容量(GB),/data1(使用率),网卡mac,是否虚拟主机"

###打开一个.csv文件，以便写入
ret_file = open("hostinfo.csv", "w")
###首先写入开头，有点字段名的意思
ret_file.write(cols + "\n")
try:
    for i in grains.keys():
        ###去掉127.0.0.1这个地址
        hostname = grains[i]["nodename"]
        ipv4 = str(grains[i]["ipv4"]).replace("'127.0.0.1',", "")
        ipv4 = ipv4.replace(",", "|")
        mem = grains[i]["mem_total"] / 1024 + 1
        num_cpu = grains[i]["num_cpus"]
        OS = grains[i]["os"] + ' ' + grains[i]["osrelease"]
        cpu = grains[i]["cpu_model"]
        virtual = grains[i]["virtual"]

        ##磁盘容量
        if "/" not in diskusage[i]:
            disk_used = " "
            disk_capacity = " "
        else:
            disk_used = float(diskusage[i]["/"]["1K-blocks"]) / 1048576
            disk_capacity = diskusage[i]["/"]["capacity"]
        if "/data" not in diskusage[i]:
            disk_data_used = " "
            disk_data_capacity = " "
        else:
            disk_data_used = float(diskusage[i]["/data"]["1K-blocks"]) / 1048576
            disk_data_capacity = diskusage[i]["/data"]["capacity"]

        if "/data1" not in diskusage[i]:
            disk_data1_used = " "
            disk_data1_capacity = " "
        else:
            disk_data1_used = float(diskusage[i]["/data"]["1K-blocks"]) / 1048576
            disk_data1_capacity = diskusage[i]["/data"]["capacity"]

        ####获取网卡mac信息
        # if "eth0" not in grains[i]["hwaddr_interfaces"]:
        #     eth0=" "
        # else:
        #     eth0=grains[i]["hwaddr_interfaces"]["eth0"]
        #
        # if "eth1" not in grains[i]["hwaddr_interfaces"]:
        #     eth1=" "
        # else:
        #     eth1=grains[i]["hwaddr_interfaces"]["eth1"]
        grains[i]["hwaddr_interfaces"].pop("lo")
        interfaces = str(grains[i]["hwaddr_interfaces"]).replace(",", " |")

        cur.execute('select hostname from hostinfo')  ###获取资产列表中的主机名
        L = []
        for host in cur.fetchall():
            L.append(host[0]);
        hostnames = ''.join(L)
        if hostname in hostnames:  ##判断主机是否已经入库，如果存在输出提示，不存在则入库
            T = [(str(ipv4), int(mem), str(cpu), int(num_cpu), str(OS), str(virtual), str(hostname))]
            sql = "update  hostinfo set IP=%s, Mem=%s ,CPU=%s, CPUs=%s, OS=%s ,virtual=%s where hostname=%s"
            cur.executemany(sql, T)
            print
            "%s 已经在资产列表！" % hostname
        else:
            T = [(str(hostname), str(ipv4), int(mem), str(cpu), int(num_cpu), str(OS), str(virtual))]
            sql = "insert into hostinfo (hostname,IP,Mem,CPU,CPUs,OS,virtual) values (%s, %s ,%s, %s, %s ,%s, %s)"
            cur.executemany(sql, T)
        ###连接并写入
        c = ","
        line = hostname + c + ipv4 + c + str(mem) + c + str(cpu) + c + str(num_cpu) + c + str(OS) + c + str(
            disk_used) + c + str(disk_capacity) + c + str(
            disk_data_used) + c + str(disk_data_capacity) + c + str(disk_data1_used) + c + str(
            disk_data1_capacity) + c + interfaces + c + str(virtual)
        ret_file.write(line + "\n")
except Exception, e:
    print
    "Exception:\n", e
finally:
    ret_file.close()
    cur.close()
    db.close()
