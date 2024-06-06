#!/usr/bin/env python
# -*- coding:utf-8 -*-


import json
import smtplib
import time
import requests
from email.mime.text import MIMEText
from django.http import HttpResponse
from apps.myapp import models
from myweb.settings import *


class AlertSender:
    def __init__(self):
        self.smtp = smtplib.SMTP()
        self.headers = {
            "Content-Type": "application/json",
            "Accept-Charset": "UTF-8"
        }

    def send_email(self, email_host, email_user, email_pass, subject, send_from, send_to, content):
        try:
            msg = MIMEText(content, "plain", 'utf-8')
            msg['Subject'] = subject
            msg['From'] = send_from
            msg['To'] = send_to

            self.smtp.connect(email_host)
            self.smtp.login(user=email_user, password=email_pass)
            self.smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
            return "Email sent successfully"
        except Exception as e:
            return str(e)

    def send_welkin(self, url, uuid, content):
        try:
            timestamp = int(time.time() * 1000)
            data = {
                "messageType": "text",
                "content": {
                    "text": content,
                },
                "timeStamp": timestamp,
                "uuid": uuid,
                "isAtAll": False
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.text
        except Exception as e:
            return str(e)

    def send_dingtalk(self, url, title, content):
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content
                }
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.text
        except Exception as e:
            return str(e)
