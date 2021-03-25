#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import socket
ip_port=('127.0.0.1',9000)
sk = socket.socket()
sk.connect(ip_port)

while True:
    receive_data = sk.recv(1024).decode()
    print(receive_data)
    inp = input('请输入：')
    sk.sendall(str(inp).encode())
    if inp == 'exit':
        break

sk.close()