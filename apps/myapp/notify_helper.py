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
        self.headers = {
            "Content-Type": "application/json",
            "Accept-Charset": "UTF-8"
        },
        self.smtp = None

    def send_email(self, email_host, email_user, email_pass, subject, send_from, send_to, content):
        try:
            msg = MIMEText(content, "plain", 'utf-8')
            msg['Subject'] = subject
            msg['From'] = send_from
            msg['To'] = send_to

            # 判断是否使用tls ssl等加密
            if EMAIL_USE_TLS:
                # Initialize the SMTP connection
                self.smtp = smtplib.SMTP(email_host, 587)  # Port 587 is typically used for TLS
                # Secure the SMTP connection with TLS
                self.smtp.starttls()
            elif EMAIL_USE_SSL:
                # Initialize the SMTP connection with SSL
                self.smtp = smtplib.SMTP_SSL(email_host, 465)  # Port 465 is typically used for SSL
            else:
                # Initialize the SMTP connection without encryption
                self.smtp = smtplib.SMTP(email_host)

            # Log in to the SMTP server
            self.smtp.login(user=email_user, password=email_pass)

            # Send the email
            self.smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())

            # Quit the SMTP server
            self.smtp.quit()

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
