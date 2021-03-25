#!/usr/bin/env python
# coding:utf-8
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.1.6',port=22,username='root',password='fd#11051045')
stdin,stdout,stderr = ssh.exec_command('ip a')
result = stdout.read()
print(result)
ssh.close()

