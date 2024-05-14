#!/usr/bin/env python
# coding:utf-8


import json
import requests
from django.http import HttpResponse
from django.shortcuts import render_to_response
from apps.myapp import common
from apps.myapp import page_helper
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from myweb.settings import *
import time
from apps.myapp import models

"""
class PromTools:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api/v1/alerts' % self.address
        self.header = {"Content-Type": "text/plain"}

    def alert_get(self):
        try:
            ret = requests.get(self.url, auth=(self.username, self.password), timeout=5, )
            # print(json.loads(ret.text))
            result = ret.text
        except Exception as e:
            # print ("Error as ",e)
            result = ' '
        return result


'''
if __name__ == "__main__":
    for prom_addres in prometheus_addresses:
        address,username,password = prom_addres.split(',')
        p = PromTools(address=address, username=username, password=password)
        content = p.alert_get()
    print    (content)
'''


@custom_login_required
@custom_permission_required('myapp.view_monitor')
def prometheus_alert(request, *args, **kwargs):
    server = PromTools(PROM_URL, PROM_USER, PROM_PASSWROD)
    try:
        alerts = json.loads(server.alert_get())['data']['alerts']
        count = len(alerts)
        page = common.try_int(kwargs['page'], 1)
        perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
        pageinfo = page_helper.pageinfo(page, count, perItem)
        alerts = alerts[pageinfo.start:pageinfo.end]
        page_string = page_helper.pager_prometheus_alert_list(request, page, pageinfo.pageCount)
        user_dict = request.session.get('is_login', None)
        wf_dict = request.session.get('wf', None)
        msg = {'alerts': alerts, 'count': count, 'pageCount': pageinfo.pageCount,
               'page': page_string, 'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('monitor/prometheus.html', msg)
    except:
        return render_to_response('500.html')


def prometheus_alert_count(*args, **kwargs):
    try:
        server = PromTools(PROM_URL, PROM_USER, PROM_PASSWROD)
        msg = json.loads(server.alert_get())
        result = len(msg['data']['alerts'])
    except:
        result = None
    return result
"""


# 2024/01/19 Powered by chatgpt
def send_alert(request, *args, **kwargs):
    # 将 JSON 数据解析为 Python 字典
    webhook_data_dict = json.loads(request.body.decode())
    # 打印原始信息
    print(f"webhook_data_dict: {webhook_data_dict}")

    # 提取关键信息
    group_labels = webhook_data_dict.get('groupLabels', {})
    common_labels = webhook_data_dict.get('commonLabels', {})
    common_annotations = webhook_data_dict.get('commonAnnotations', {})
    alerts = webhook_data_dict.get('alerts', [])

    # 打印一些信息，实际情况下可以根据需求进行处理
    print(f"Group Labels: {group_labels}")
    print(f"Common Labels: {common_labels}")
    print(f"Common Annotations: {common_annotations}")

    for alert in alerts:
        alert_status = alert.get('status', '')
        alert_labels = alert.get('labels', {})
        alert_annotations = alert.get('annotations', {})
        starts_at = alert.get('startsAt', '')
        ends_at = alert.get('endsAt', '')
        generator_url = alert.get('generatorURL', '')

        # 打印或处理告警信息
        print(f"Status: {alert_status}, Alert: {alert_labels}, Annotations: {alert_annotations}")
        print(f"Starts At: {starts_at}, Ends At: {ends_at}, Generator URL: {generator_url}")
        print("=" * 60)

        # 生成格式化内容
        formatted_content = f"告警状态： {alert_status.upper()}\n\n"
        formatted_content += f"告警名称： {alert_labels['alertname']}\n\n"
        formatted_content += f"告警级别： {alert_labels['severity']}\n\n"
        formatted_content += f"实例地址： {alert_labels['instance']}\n\n"
        formatted_content += f"告警摘要： {alert_annotations.get('summary', '')}\n\n"
        formatted_content += f"告警详情： {alert_annotations.get('description', '')}\n\n"
        formatted_content += f"触发时间： {common.time_tz_fmt(starts_at)}\n\n"
        formatted_content += f"结束时间： {common.time_tz_fmt(ends_at)}\n\n"
        # formatted_content += f"Generator URL: {generator_url}"

        # 打印格式化后信息
        print(f"formatted_content: {formatted_content}")

        # webhook告警
        '''
        # 钉钉
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【Prometheus监控告警】 " + {alert_labels['alertname']},
                "text": formatted_content
            }
        }
        headers = {"Content-Type": "application/json"}
        '''
        # weLink
        # 时间戳，毫秒计算
        timestamp = time.time() * 1000
        data = {
            "messageType": "text",
            "content": {
                "text": formatted_content,
            },
            # "timeStamp": i["startTime"],
            "timeStamp": timestamp,
            # 测试
            # "uuid": PROM_WELINK_UUID,
            # 生产
            "uuid": PROM_WELINK_UUID,
            "isAtAll": False
        }
        headers = {
            "Content-Type": "application/json",
            "Accept-Charset": "UTF-8"
        }

        try:
            ret_dict = {}
            '''
            # 钉钉
            ret_dingtalk = requests.post(PROM_DINGTALK_WEBHOOK_URL, json=data, headers=headers)
            # print(ret_dingtalk.text)
            '''
            # weLink
            ret_welink = requests.post(PROM_WELINK_WEBHOOK_URL, json=data, headers=headers)
            # print(ret_welink.text)

            # ret_dict["ret_dingtalk"] = ret_dingtalk.text
            ret_dict["ret_welink"] = ret_welink.text

            # 告警存入数据库
            models.MonitorPrometheus.objects.create(status=alert_status, alertname=alert_labels['alertname'],
                                                    severity=alert_labels['severity'],
                                                    instance=alert_labels['instance'],
                                                    summary=alert_labels['summary'],
                                                    description=alert_labels['description'],
                                                    starts_at=alert_labels['starts_at'],
                                                    ends_at=alert_labels['ends_at'])

            return HttpResponse(json.dumps(ret_dict))
        except Exception as e:
            # print(e)
            return HttpResponse(e)


@custom_login_required
def dashboard(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'login_user': user_dict['user'], 'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('monitor/prometheus_dashboard.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_monitorprometheus')
def prometheus_alert(request, *args, **kwargs):
    try:
        qs_alerts = models.MonitorPrometheus.objects.all()
        count = qs_alerts.count()
        page = common.try_int(kwargs['page'], 1)
        perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
        pageinfo = page_helper.pageinfo(page, count, perItem)
        qs_alerts_paged = qs_alerts[pageinfo.start:pageinfo.end]
        page_string = page_helper.pager_prometheus_alert_list(request, page, pageinfo.pageCount)
        user_dict = request.session.get('is_login', None)
        wf_dict = request.session.get('wf', None)
        msg = {'alerts': qs_alerts_paged, 'count': count, 'pageCount': pageinfo.pageCount,
               'page': page_string, 'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('monitor/prometheus.html', msg)
    except:
        return render_to_response('500.html', msg, status=500)
