#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket

ip_port = ('127.0.0.1',8000)
sk = socket.socket()
sk.connect(ip_port)

while True:
    inp = input('请输入：')
    if inp == 'exit':
        break
    else:
        sk.sendall(str(inp).encode())
sk.close()


