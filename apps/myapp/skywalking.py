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
    data_dict = json.loads(request.body.decode())
    # 打印原始信息
    print("=" * 60)
    print("data_dict：", data_dict, type(data_dict))

    for alert in data_dict:
        alter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(alert["startTime"]) / 1000))
        formatted_content = """警告时间：%s \n\n警告类型：%s \n\n服务名称：%s \n\n规则名称：%s \n\n详细内容：%s""" % (
            alter_time, alert["scope"], alert["name"], alert["ruleName"], alert["alarmMessage"])
        print("formatted_content：", formatted_content)

        # 发送邮件配置
        msg = MIMEText(formatted_content, "plain", 'utf-8')
        msg['Subject'] = SKYWALKING_EMAIL_SUBJECT
        msg['From'] = EMAIL_SEND_FROM
        msg['To'] = SKYWALKING_EMAIL_RECEIVER
        smtp = smtplib.SMTP()
        smtp.connect(EMAIL_HOST)
        smtp.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)

        # webhook告警配置
        '''
        # 钉钉
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【Skywalking监控告警】 " + alert['name'],
                "text": formatted_content
            }
        }
        headers = {"Content-Type": "application/json"}
        '''
        # weLink
        timestamp = time.time() * 1000
        data = {
            "messageType": "text",
            "content": {
                "text": formatted_content,
            },
            # "timeStamp": alert["startTime"],
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
            ret_dict = {}
            # Email告警发送
            # Email
            ret_email = smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
            # print(ret_email)
            # webhook告警发送
            '''
            # 钉钉
            ret_dingtalk = requests.post(SKYWALKING_DINGTALK_WEBHOOK_URL, json=data, headers=headers)
            # print(ret_dingtalk.text)
            '''
            # weLink
            ret_welink = requests.post(SKYWALKING_WELINK_WEBHOOK_URL, json=data, headers=headers)
            # print(ret_welink.text)

            # ret_dict["ret_dingtalk"] = ret_dingtalk.text
            ret_dict["ret_email"] = ret_email
            ret_dict["ret_welink"] = ret_welink.text

            return HttpResponse(json.dumps(ret_dict))
        except Exception as e:
            # print(e)
            return HttpResponse(e)
