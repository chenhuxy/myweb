#!/usr/bin/env python
# coding:utf-8

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import time
from apps.myapp import models
from celery.result import AsyncResult
from django.shortcuts import render_to_response
from apps.myapp.auth_helper import custom_login_required
from django.shortcuts import HttpResponse
from myweb.settings import SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, SSH_CMD, SSH_WORKDIR, SSH_SCRIPT_NAME


# 一个链接（channel）创建时，通过group_add将channel添加到Group中，链接关闭通过group_discard将channel从Group中剔除，收到消息时可以调用group_send方法将消息发送到Group，这个Group内所有的channel都可以收的到
# 当我们启用了channel layer之后，所有与consumer之间的通信将会变成异步的，所以必须使用async_to_sync

class TasklogConsumer(WebsocketConsumer):
    def connect(self):
        self.channel_group_name = 'task_log'
        print('WebSocket建立连接：', self.channel_group_name)

        # 加入通道层
        # async_to_sync(…)包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用的是异步通道层方法。(所有通道层方法都是异步的。)
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name,
            self.channel_name
        )

        # 接受WebSocket连接。
        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name,
            {
                'type': 'get_message',
            }
        )

    def disconnect(self, close_code):
        print('WebSocket关闭连接')
        # 离开通道
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group_name,
            self.channel_name
        )

    # 从WebSocket中接收消息
    def receive(self, text_data=None, bytes_data=None):
        print('WebSocket接收消息：', text_data, type(text_data))
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        proj_id = text_data_json['proj_id']
        proj_name = text_data_json['proj_name']
        tag = text_data_json['tag']
        task_id = text_data_json['task_id']
        id = text_data_json['id']
        # print("receive message",message,type(message))
        # 发送消息到通道
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name,
            {
                'type': 'get_message',  # group_send中的type指定了消息处理的函数，这里会将消息转给get_message函数去处理
                'message': message,
                'proj_id': proj_id,
                'proj_name': proj_name,
                'tag': tag,
                'task_id': task_id,
                'id': id,
            }
        )

    # 从通道中接收消息
    def get_message(self, event):
        # print("event",event,type(event))
        if event.get('message'):
            message = event['message']
            proj_id = event['proj_id']
            proj_name = event['proj_name']
            tag = event['tag']
            task_id = event['task_id']
            id = event['id']
            # 判断消息
            if message == "close":
                # 关闭websocket连接
                self.disconnect(self.channel_group_name)
                print("前端关闭websocket连接")

            # 判断消息，执行脚本
            if message == "来自客户端浏览器的请求信息":

                # self.scope类似于django中的request，包含了请求的type、path、header、cookie、session、user等等有用的信息
                # userDict = self.scope.session.get('is_login', None)

                # 判断任务是否执行完成，数据库是否存在日志记录
                task_log = models.deploy_list_detail.objects.filter(task_id=task_id).values('task_log')[0]['task_log']
                # print(task_log)

                # 如果执行完成则从数据库读取
                if task_log is not None:
                    self.send(text_data=json.dumps(task_log))
                    # print('已发送：' + task_log)

                # 如果还在执行则从远程读取
                else:
                    try:
                        remote_file_name = SSH_WORKDIR + '/logs/' + proj_name + '/' + SSH_SCRIPT_NAME + '-' + id + '.log'
                        print(remote_file_name)
                        transport = paramiko.Transport((SSH_HOST, SSH_PORT))
                        transport.connect(username=SSH_USERNAME, password=SSH_PASSWORD)
                        ssh = paramiko.SSHClient()
                        ssh._transport = transport
                        sftp = ssh.open_sftp()
                        remote_file = sftp.open(remote_file_name)
                        while True:
                            # nextline = remote_file.readline().strip()
                            nextline = remote_file.readline()
                            # print(nextline)

                            # 发送消息到客户端
                            self.send(text_data=json.dumps(nextline))

                            flag = nextline.endswith('EOF\n')
                            if flag:
                                remote_file.seek(0, )
                                lines = remote_file.read().decode()
                                # print(lines)
                                # models.deploy_list_detail.objects.filter(task_id=task_id).update(task_log=lines,status='已完成')
                                models.deploy_list_detail.objects.filter(task_id=task_id).update(task_log=lines, )
                                break
                    except Exception as e:
                        print(e)
                    finally:
                        # 关闭打开的文件
                        remote_file.close()
                        # 关闭ssh连接
                        ssh.close()

                # 关闭websocket连接
                self.disconnect(self.channel_group_name)
                print("后端关闭websocket连接")


