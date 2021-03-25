#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import paramiko
transport = paramiko.Transport('192.168.1.6',22)
transport.connect(username='root',password='fd#11051045')
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put('D:\Program Files\Python36\LICENSE.txt','/root/licence')
sftp.get('/root/','D:\新建文件夹')
transport.close()