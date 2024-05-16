#!/usr/bin/env python
# coding:utf-8


import json
import smtplib
from email.mime.text import MIMEText
import requests
from django.shortcuts import HttpResponse

from apps.myapp import models, common, page_helper
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from myweb.settings import *
import time
from django.shortcuts import render_to_response


# 2024/1/17 增加webhook告警
def send_alert(request, *args, **kwargs):
    # 将 JSON 数据解析为 Python 字典
    data_dict = json.loads(request.body.decode())
    # 打印原始信息
    print("=" * 60)
    print("data_dict：", data_dict, type(data_dict))

    for alert in data_dict:
        alert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(alert["startTime"]) / 1000))
        formatted_content = """警告时间：%s \n\n警告类型：%s \n\n服务名称：%s \n\n规则名称：%s \n\n详细内容：%s""" % (
            alert_time, alert["scope"], alert["name"], alert["ruleName"], alert["alarmMessage"])
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

            # 告警存入数据库
            models.MonitorSkywalking.objects.create(scope=alert["scope"], name=alert["name"],
                                                    ruleName=alert["ruleName"], alarmMessage=alert["alarmMessage"],
                                                    startTime=alert_time)

            return HttpResponse(json.dumps(ret_dict))
        except Exception as e:
            # print(e)
            return HttpResponse(e)


@custom_login_required
def dashboard(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'login_user': user_dict['user'], 'wf_count_pending': wf_dict['wf_count_pending'],
           'grafana_url': GRAFANA_URL, 'skywalking_ui_url': SKYWALKING_UI_URL}
    return render_to_response('monitor/skywalking_dashboard.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_monitorskywalking')
def skywalking_alert(request, *args, **kwargs):
    try:
        qs_alerts = models.MonitorSkywalking.objects.all().order_by('-id')
        count = qs_alerts.count()
        page = common.try_int(kwargs['page'], 1)
        perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
        pageinfo = page_helper.pageinfo(page, count, perItem)
        qs_alerts_paged = qs_alerts[pageinfo.start:pageinfo.end]
        page_string = page_helper.pager_skywalking_alert_list(request, page, pageinfo.pageCount)
        user_dict = request.session.get('is_login', None)
        wf_dict = request.session.get('wf', None)
        msg = {'alerts': qs_alerts_paged, 'count': count, 'pageCount': pageinfo.pageCount,
               'page': page_string, 'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('monitor/skywalking.html', msg)
    except:
        return render_to_response('500.html', msg, status=500)
