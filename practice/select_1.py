#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket
import select

ip_port = ('127.0.0.1',8000)
sk1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk1.bind(ip_port)
sk1.listen(5)
sk1.setblocking(0)
inputs = [sk1,]
while True:
    readable_list,wirteable_list,error_list = select.select(inputs,[],inputs,1)
    for r in readable_list:
        if r == sk1:
            print('接受')
            request,address = r.accept()
            request.setblocking(0)
            inputs.append(request)
        else:
            received = r.recv(1024).decode()
            if received:
                print('received data:',received)
            else:
                inputs.remove(r)
sk1.close()




