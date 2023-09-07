#!/usr/bin/env python
#coding:utf-8


import json
import smtplib
from email.mime.text import MIMEText
import time
from myweb.settings import *
from django.shortcuts import HttpResponse


def send_mail(request,*args,**kwargs):
    info = json.loads(request.body.decode())
    # print("#########：",info, type(info))
    for i in info:
        alter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i["startTime"] / 1000))
        content = """
        警告时间:%s
        警告类型:%s
        服务名称:%s
        规则名称:%s
        详细内容:%s
        """ % (alter_time, i["scope"], i["name"], i["ruleName"], i["alarmMessage"])
        # print(content)
        # 发送邮件
        mail_sever = EMAIL_HOST
        mail_user = EMAIL_HOST_USER
        mail_pass = EMAIL_HOST_PASSWORD
        sender = EMAIL_SEND_FROM
        receiver = SKYWALKING_EMAIL_RECEIVER
        msg = MIMEText(content, "plain", 'utf-8')
        msg['Subject'] = SKYWALKING_EMAIL_SUBJECT
        msg['From'] = sender
        msg['To'] = receiver
        smtp = smtplib.SMTP()
        smtp.connect(mail_sever)
        smtp.login(user=mail_user,password=mail_pass)
        smtp.sendmail(sender,receiver.split(','),msg.as_string())
    return HttpResponse("邮件发送成功")
