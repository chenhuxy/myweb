#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import  paramiko
transport = paramiko.Transport(('192.168.1.6',22))
transport.connect(username='root',password='fd#11051045')
ssh = paramiko.SSHClient()
ssh._transport = transport
stdin,stdout,stderr = ssh.exec_command('ifconfig')
result = stdout.read()
print(result)
ssh.close()