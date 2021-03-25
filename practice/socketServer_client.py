#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import socket

ip_port = ('127.0.0.1',6000)
client = socket.socket()
client.connect(ip_port)
client.settimeout(5)

while True:
    data = client.recv(1024).decode()
    print(data)
    inp = input('请输入：')
    client.sendall(str(inp).encode())
    if inp == 'exit':
        break
data2= client.recv(1024).decode()
print(data2)
client.close()



