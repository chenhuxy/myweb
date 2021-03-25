#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import getpass
import paramiko
import select
import os
import sys
user = input('username:')
pwd = getpass.getpass('password')
if user == 'alex' and pwd == '123':
    print('登录成功！')
else:
    print('登录失败！')

dict = {
    'alex':['192.168.1.6',
            '192.168.1.7',
            'c10.puppet.com',
            ],
    'eric':['c110.puppet.com',]
}
host_list = dict['alex']
print('please select:')
for index,item in enumerate(host_list,1):
    print(index,item)
inp = input('your select (NO):')
inp = int(inp)
hostname = host_list[inp-1]
prot = 22

tran= paramiko.Transport((hostname,port,))
tran.start_client()
default_path = os.path.join(os.environ['HOME'],'.ssh','id_rsa')
key = paramiko.RSAKey.from_private_key_file(default_path)
tran.auth_publickey('root',key)

chan = tran.open_session()
chan.get_pty()
chan.invoke_shell()
chan.close()
tran.close()

while True:
    readable,writeadble,error = select.select([chan,sys.stdin,],[],[],1)
    if chan in readable:
        try:
            x = chan.recv(1024)
            if len(x) == 0:
                print('\r\n *** EOF \r\n')
                break
            sys.stdout.write(x)
            sys.stdout.flush()
        except socket.timeout:
            pass
    if sys.stdin in readable:
        inp = sys.stdin.readline()
        chan.sendall(inp)



