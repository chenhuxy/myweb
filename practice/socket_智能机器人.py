#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import socket
ip_port = ('127.0.0.1',9000)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    conn,address = sk.accept()
    conn.sendall(str('欢迎致电10086,1..,2,,,0人工服务').encode())
    flag = True
    while flag:
        data = conn.recv(1024).decode()
        if data == 'exit':
            flag = False
        elif data == '0':
            conn.sendall(str('您的通话可能被录音。。。').encode())
        else:
            conn.sendall(str('请重新输入').encode())

    conn.close()





