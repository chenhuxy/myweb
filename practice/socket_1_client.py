#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket
ip_port = ('127.0.0.1',8888)
sk = socket.socket()
sk.connect(ip_port)
data = str.encode('请求占领地球')
sk.sendall(data)
server_reply = sk.recv(1024).decode()
print(server_reply)
sk.close()