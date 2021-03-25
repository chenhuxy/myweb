#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import socketserver

ip_port = ('127.0.0.1',6000)

class myServer(socketserver.BaseRequestHandler):
   def handle(self):
       conn = self.request
       conn.sendall(str('欢迎致电10086。。xx请按1，oo请按2，人工请按0').encode())
       flag = True
       while flag:
           data = conn.recv(1024).decode()
           print(data)
           if data == 'exit':
               conn.sendall(str('bye').encode())
               flag = False
           elif data == '0':
               conn.sendall(str('已为您转接人工，您的通话可能被录音。。').encode())
           else:
               conn.sendall(str('输入错误，xx请按1，oo请按2，人工请按0').encode())
if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(ip_port,myServer)
    server.serve_forever()




