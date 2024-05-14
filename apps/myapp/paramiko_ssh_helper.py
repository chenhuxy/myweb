#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import paramiko


def ssh_remote(ip, port, username, password, cmd, arg1, arg2, arg3):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd + '' + arg1 + '' + arg2 + '' + arg3)
    result = stdout.read()
    ssh.close()
    print(result)
    return result
