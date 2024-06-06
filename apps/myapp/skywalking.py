#!/usr/bin/env python
# coding:utf-8


import json
import smtplib
from email.mime.text import MIMEText
import requests
from django.shortcuts import HttpResponse
from apps.myapp import models, common, page_helper, notify_helper
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from myweb.settings import *
import time
from django.shortcuts import render_to_response


# 2024/1/17 增加webhook告警
def send_alert(request, *args, **kwargs):
    try:
        # 将 JSON 数据解析为 Python 字典
        data_dict = json.loads(request.body.decode())
        print("=" * 60)
        print("data_dict：", data_dict, type(data_dict))

        ret_dict = {}
        alert_sender = notify_helper.AlertSender()

        for alert in data_dict:
            alert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(alert["startTime"]) / 1000))
            formatted_content = """警告时间：%s \n\n警告类型：%s \n\n服务名称：%s \n\n规则名称：%s \n\n详细内容：%s""" % (
                alert_time, alert["scope"], alert["name"], alert["ruleName"], alert["alarmMessage"])
            print("formatted_content：", formatted_content)

            try:
                # Email告警发送
                email_msg = MIMEText(formatted_content, "plain", 'utf-8')
                email_msg['Subject'] = SKYWALKING_EMAIL_SUBJECT
                email_msg['From'] = EMAIL_SEND_FROM
                email_msg['To'] = ', '.join(SKYWALKING_EMAIL_RECEIVER)
                ret_email = alert_sender.send_email(EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, email_msg)
                ret_dict["ret_email"] = ret_email

                '''
                # 钉钉告警发送
                ret_dingtalk = alert_sender.send_dingtalk(SKYWALKING_DINGTALK_WEBHOOK_URL,
                                                          f"【Skywalking监控告警】 {alert['name']}",
                                                          formatted_content)
                ret_dict["ret_dingtalk"] = ret_dingtalk.text
                '''

                # weLink告警发送
                ret_welink = alert_sender.send_welink(SKYWALKING_WELINK_WEBHOOK_URL, SKYWALKING_WELINK_UUID,
                                                      formatted_content)
                ret_dict["ret_welink"] = ret_welink.text

                # 告警存入数据库
                models.MonitorSkywalking.objects.create(
                    scope=alert["scope"],
                    name=alert["name"],
                    ruleName=alert["ruleName"],
                    alarmMessage=alert["alarmMessage"],
                    startTime=alert_time
                )
            except Exception as alert_exception:
                print(f"Error processing alert: {alert_exception}")
                ret_dict["error"] = str(alert_exception)
                continue

        return HttpResponse(json.dumps(ret_dict), content_type="application/json")
    except Exception as e:
        print(f"Error in send_alert: {e}")
        return HttpResponse(json.dumps({"error": str(e)}), status=500, content_type="application/json")


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
    except Exception as e:
        msg = str(e)
        return render_to_response('500.html', msg, status=500)
