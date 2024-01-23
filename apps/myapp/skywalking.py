#!/usr/bin/env python
# coding:utf-8


import json
import smtplib
from email.mime.text import MIMEText
import requests
from django.shortcuts import HttpResponse
from myweb.settings import *
import time


# 2024/1/17 增加webhook告警
def send_alert(request, *args, **kwargs):
    # 将 JSON 数据解析为 Python 字典
    info = json.loads(request.body.decode())
    # 打印原始信息
    print("=" * 60)
    print("info：", info, type(info))

    for i in info:
        alter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i["startTime"]) / 1000))
        content = """警告时间：%s \n\n警告类型：%s \n\n服务名称：%s \n\n规则名称：%s \n\n详细内容：%s""" % (
            alter_time, i["scope"], i["name"], i["ruleName"], i["alarmMessage"])
        print(content)
        # 发送邮件
        msg = MIMEText(content, "plain", 'utf-8')
        msg['Subject'] = SKYWALKING_EMAIL_SUBJECT
        msg['From'] = EMAIL_SEND_FROM
        msg['To'] = SKYWALKING_EMAIL_RECEIVER
        smtp = smtplib.SMTP()
        smtp.connect(EMAIL_HOST)
        smtp.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)

        try:
            status_email = smtp.sendmail(EMAIL_SEND_FROM, SKYWALKING_EMAIL_RECEIVER.split(','), msg.as_string())
        except Exception as e:
            status_email = e
        # print(status_email)

        # webhook告警
        '''
        # 钉钉
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【Skywalking监控告警】 " + i['name'],
                "text": content
            }
        }
        headers = {"Content-Type": "application/json"}
        '''
        # weLink
        timestamp = time.time() * 1000
        data = {
            "messageType": "text",
            "content": {
                "text": content,
            },
            # "timeStamp": i["startTime"],
            "timeStamp": timestamp,
            # 测试
            # "uuid": SKYWALKING_WELINK_UUID,
            # 生产
            "uuid": SKYWALKING_WELINK_UUID,
            "isAtAll": False
        }
        headers = {
            "Content-Type": "application/json",
            "Accept-Charset": "UTF-8"
        }

        try:
            '''
            # 钉钉
            r = requests.post(SKYWALKING_DINGTALK_WEBHOOK_URL, json=data, headers=headers)
            '''
            # weLink
            r = requests.post(SKYWALKING_WELINK_WEBHOOK_URL, json=data, headers=headers)

            # print(r.text)
            status_webhook = r.text
        except Exception as e:
            status_webhook = e
    # print(status_webhook)

    return HttpResponse("webhook：" + status_webhook)
    # return HttpResponse("邮件：" + status_email, "webhook：" + status_webhook)
