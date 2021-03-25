#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket


def HandlerReuest(client):
    buf = client.recv(1024)
    print (client.send(str.encode('HTTP/1.1 200 OK \r\n\r\n')))
    print (client.send(str.encode('hello world')))

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('localhost',8080))
    sock.listen(5)
    print('server start at localhost:8080...')

    while True:
        conn,address = sock.accept()
        HandlerReuest(conn)
        conn.close()

if __name__ == '__main__':
    main()
