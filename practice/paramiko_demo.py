#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import paramiko
import uuid
class Haproxy(object):
    def __init__(self):
        self.host = '192.168.1.6'
        self.port = 22
        self.username = 'root'
        self.password = 'fd#11051045'
        self.__k = None

    def create_file(self):
        file_name = str(uuid.uuid4())
        with open(file_name,'w') as f:
            f.write('sb')
            return file_name

    def run(self):
        self.connect()
        self.upload()
        self.rename()
        self.close()

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self):
        file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(file_name,'/root/1.py')

    def rename(self):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin,stdout,stderr = ssh.exec_command('mv /root/1.py /root/hehe.py')
        result = stdout.read()

ha = Haproxy()
ha.run()


