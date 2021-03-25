#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket
ip_port = ('127.0.0.1',8888)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print('server is waiting...')
    conn,addr = sk.accept()
    client_data = conn.recv(1024).decode()
    print(client_data)
    data = str.encode('不要回答')
    conn.sendall(data)
    conn.close()


