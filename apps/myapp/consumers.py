#!/usr/bin/env python
# coding:utf-8

import json
import os
import re

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
from myweb.settings import *

"""
# 一个链接（channel）创建时，通过group_add将channel添加到Group中，链接关闭通过group_discard将channel从Group中剔除，
  收到消息时可以调用group_send方法将消息发送到Group，这个Group内所有的channel都可以收的到
# 当我们启用了channel layer之后，所有与consumer之间的通信将会变成异步的，所以必须使用async_to_sync
"""


class TasklogConsumer(WebsocketConsumer):
    def connect(self):
        self.channel_group_name = 'task_log'
        print('WebSocket建立连接：', self.channel_group_name)

        """
        # async_to_sync(…)包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用的是异步通道层方法(所有通道层方法都是异步的)
        """

        # 加入通道层
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name,
            self.channel_name
        )

        # 接受WebSocket连接
        self.accept()

        # 初始发送消息
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
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            proj_id = text_data_json['proj_id']
            proj_name = text_data_json['proj_name']
            tag = text_data_json['tag']
            task_id = text_data_json['task_id']
            deploy_id = text_data_json['id']
        except (TypeError, json.JSONDecodeError) as e:
            print(f"JSON decode error: {e}")
            return
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
                'id': deploy_id,
            }
        )

    # 从通道中接收消息
    def get_message(self, event):
        # print("event",event,type(event))
        if 'message' not in event:
            return

        message = event['message']
        proj_id = event['proj_id']
        proj_name = event['proj_name']
        tag = event['tag']
        task_id = event['task_id']
        deploy_id = event['id']

        # 判断消息
        if message == "close":
            # 关闭websocket连接
            self.disconnect(self.channel_group_name)
            print("前端关闭websocket连接")

        # 判断消息，执行脚本
        elif message == "来自客户端浏览器的请求信息":

            # self.scope类似于django中的request，包含了请求的type、path、header、cookie、session、user等等有用的信息
            # userDict = self.scope.session.get('is_login', None)

            # 判断任务是否执行完成，数据库是否存在日志记录
            task_log = models.deploy_list_detail.objects.filter(task_id=task_id).values('task_log').first()
            task_log = task_log['task_log'] if task_log else None

            # print(task_log)

            log_dir = os.path.join(ANSIBLE_BASE_DIR, 'logs')  # 设置日志目录
            log_file_path = os.path.join(log_dir, f"ansible_deploy-{deploy_id}.log")

            # 如果执行完成则从数据库读取
            if task_log is not None:
                self.send(text_data=json.dumps(task_log))
                print('已发送数据库日志：' + task_log)

            # 如果还在执行则从远程读取
            else:
                try:
                    with open(log_file_path, 'r', encoding='utf-8') as log_file:
                        while True:
                            nextline = log_file.readline()
                            if nextline:
                                # self.send(text_data=json.dumps(nextline.strip()))
                                self.send(text_data=json.dumps(nextline))
                                if nextline.strip().endswith(f"deploy_id {deploy_id} 结束----------------------"):
                                    break
                            else:
                                time.sleep(1)  # Wait for a while before trying again to avoid busy waiting

                except FileNotFoundError:
                    print(f"文件未找到: {log_file_path}")
                    # logger.error(f"文件未找到: {log_file_path}")
                except Exception as e:
                    print(f"发生错误: {e}")
                    # logger.error(f"发生错误: {e}")

            # 关闭websocket连接
            self.disconnect(self.channel_group_name)
            print("后端关闭websocket连接")


