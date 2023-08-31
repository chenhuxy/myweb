#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from __future__ import absolute_import, unicode_literals

import time

from celery import shared_task
from celery import signature

# Create your tasks here

from django.core.mail import send_mail
from django.template import loader, RequestContext
from apps.myapp import token_helper
from django.utils.safestring import mark_safe
from django.core.cache import cache
import json
from django.shortcuts import render
from apps.myapp import models
from django.shortcuts import render_to_response
from django.utils import timezone
import paramiko
from apps.myapp import loop
import logging
from django.shortcuts import redirect
from celery import group, chain, chord
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from apps.myapp import consumers
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import pickle
from myweb.settings import SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, SSH_CMD, SSH_WORKDIR
from celery.result import AsyncResult


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 30, 'countdown': 60})
def send_email(email, username):
    title = '【CMDB激活邮件】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email, ]
    fail_silently = False
    token = token_helper.get_random_uuid()
    # 加载模板
    template = loader.get_template('account/email.html')
    # 渲染模板
    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
    html_str = template.render({"username": username, 'token': token, })
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    send_mail(title, msg, send_from, send_to, fail_silently, html_message=html_str)
    # print(html_str,type(html_str))
    # 记录 token 对应的邮箱是谁 v  k
    cache.set(token, email, 600)
    # print(cache.get(token))


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def send_email_code(email, verify_code):
    title = '【CMDB找回密码邮件】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email, ]
    fail_silently = False
    # verify_code = token_helper.get_random_code()
    # 加载模板
    template = loader.get_template('account/email_code.html')
    # 渲染模板
    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
    html_str = template.render({'verify_code': verify_code, })
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    send_mail(title, msg, send_from, send_to, fail_silently, html_message=html_str)
    # print(html_str,type(html_str))
    # 记录 token 对应的邮箱是谁 v  k
    cache.set(verify_code, email, 600)
    # print(cache.get(verify_code))
    # return (verify_code)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_send_email(sn, username, email):
    title = '【流程审批提醒】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email, ]
    fail_silently = False
    template = loader.get_template('workflow/workflow_email.html')
    html_str = template.render({"username": username, 'sn': sn, })
    send_mail(title, msg, send_from, send_to, fail_silently, html_message=html_str)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def DeleteHistoryProcess(sn, ):
    models.wf_info_process_history.objects.filter(sn=sn).delete()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def UpdateCurrent(sn, status, flow_id, assignee, next_assignee):
    update_time = timezone.now()
    models.wf_info.objects.filter(sn=sn).update(status=status, update_time=update_time, flow_id=flow_id,
                                                next_assignee=next_assignee, assignee=assignee, )


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def UpdateHistoryProcess(sn, title, sponsor, type_id, content, status, business_id, flow_id, assignee, next_assignee,
                         memo, suggest, suggest_content, proj_name, proj_tag, proj_id):
    models.wf_info_process_history.objects.create(sn=sn, title=title, sponsor=sponsor, type_id=type_id,
                                                  content=content, status=status, business_id=business_id,
                                                  flow_id=flow_id, assignee=assignee, next_assignee=next_assignee,
                                                  memo=memo,
                                                  suggest=suggest, suggest_content=suggest_content,
                                                  proj_name=proj_name, proj_tag=proj_tag, proj_id=proj_id)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_commit(sn):
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_business = models.wf_business.objects.filter(wf_info__sn=sn)
    length = wf_business.values_list('approval', flat=True).count()
    order_list = []
    for i in range(length):
        approval_id = wf_business.values_list('approval', flat=True)[i]
        worklow_order = models.userInfo.objects.filter(id=approval_id).values('workflow_order')[0]['workflow_order']
        order_list.append(worklow_order)
    order_list_sorted = sorted(order_list)
    title = wf_info.values('title')[0]['title']
    sponsor = wf_info.values('sponsor')[0]['sponsor']
    type_id = wf_info.values('type')[0]['type']
    content = wf_info.values('content')[0]['content']
    # 2023/08/17
    proj_name = wf_info.values('proj_name')[0]['proj_name']
    proj_tag = wf_info.values('proj_tag')[0]['proj_tag']
    proj_id = wf_info.values('proj_id')[0]['proj_id']

    status = '已提交'
    business_id = wf_info.values('business')[0]['business']
    flow_id = 0
    assignee_username = sponsor
    next_assignee_username = models.userInfo.objects.filter(workflow_order=order_list_sorted[0]).values('username')[0][
        'username']
    next_assignee_email = models.userInfo.objects.filter(workflow_order=order_list_sorted[0]).values('email')[0][
        'email']
    print(order_list_sorted[0], next_assignee_username, next_assignee_email, order_list_sorted, )
    memo = wf_info.values('memo')[0]['memo']
    suggest = None
    suggest_content = None
    (group(UpdateCurrent.s(sn, status, flow_id, assignee_username, next_assignee_username),
           UpdateHistoryProcess.s(sn, title,
                                  sponsor, type_id, content, status, business_id, flow_id, assignee_username,
                                  next_assignee_username, memo, suggest, suggest_content, proj_name, proj_tag, proj_id)
           ) | workflow_send_email.si(sn, next_assignee_username, next_assignee_email))()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_withdraw(sn):
    status = '未提交'
    flow_id = -1
    assignee_username = ''
    next_assignee_username = ''
    (DeleteHistoryProcess.s(sn) | UpdateCurrent.si(sn, status, flow_id, assignee_username, next_assignee_username))()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_process(sn, suggest, suggest_agree, suggest_reject, ):
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_business = models.wf_business.objects.filter(wf_info__sn=sn)
    length = wf_business.values_list('approval', flat=True).count()
    flow_id = wf_info.values('flow_id')[0]['flow_id']
    type_id = wf_info.values('type')[0]['type']
    sponsor = wf_info.values('sponsor')[0]['sponsor']
    sponsor_username = sponsor
    sponsor_email = models.userInfo.objects.filter(username=sponsor_username).values('email')[0]['email']
    title = wf_info.values('title')[0]['title']
    content = wf_info.values('content')[0]['content']
    business_id = wf_info.values('business')[0]['business']
    memo = wf_info.values('memo')[0]['memo']

    # 2023/08/17
    proj_name = wf_info.values('proj_name')[0]['proj_name']
    proj_tag = wf_info.values('proj_tag')[0]['proj_tag']
    proj_id = wf_info.values('proj_id')[0]['proj_id']
    unit = models.wf_business.objects.filter(id=business_id).values('name')[0]['name']
    deploy_status = '执行中'
    try:
        max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
    except:
        # 如果数据库为空，则从 ID 为 1 的数据开始提取
        max_id = 0
    print(max_id, type(max_id))

    order_list = []
    for i in range(length):
        approval_id = wf_business.values_list('approval', flat=True)[i]
        worklow_order = models.userInfo.objects.filter(id=approval_id).values('workflow_order')[0]['workflow_order']
        order_list.append(worklow_order)
    order_list_sorted = sorted(order_list)
    for i in range(flow_id, length):
        assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i])
        assignee_username = assignee.values('username')[0]['username']
        assignee_email = assignee.values('email')[0]['email']
        flow_id = flow_id + 1
        if suggest == '同意':
            suggest_content = suggest_agree
            if flow_id < length:
                status = '处理中'
                next_assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i + 1])
                next_assignee_username = next_assignee.values('username')[0]['username']
                next_assignee_email = next_assignee.values('email')[0]['email']
                username = next_assignee_username
                email = next_assignee_email
                (group(UpdateCurrent.s(sn, status, flow_id, assignee_username, next_assignee_username),
                       UpdateHistoryProcess.s(sn, title,
                                              sponsor, type_id, content, status, business_id, flow_id,
                                              assignee_username, next_assignee_username, memo, suggest, suggest_content,
                                              proj_name, proj_tag, proj_id)
                       ) | workflow_send_email.si(sn, username, email))()
            else:
                status = '已完成'
                next_assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i])
                next_assignee_username = next_assignee.values('username')[0]['username']
                next_assignee_email = next_assignee.values('email')[0]['email']
                username = sponsor_username
                email = sponsor_email
                # 判断工单类型是否‘生产发布’
                if proj_name:
                    (group(UpdateCurrent.s(sn, status, flow_id, assignee_username, next_assignee_username),
                           UpdateHistoryProcess.s(sn, title,
                                                  sponsor, type_id, content, status, business_id, flow_id,
                                                  assignee_username,
                                                  next_assignee_username, memo, suggest, suggest_content, proj_name,
                                                  proj_tag,
                                                  proj_id)
                           ) | workflow_send_email.si(sn, username, email) | ssh_remote_exec_cmd_wf.si(SSH_HOST,
                                                                                                       SSH_PORT,
                                                                                                       SSH_USERNAME,
                                                                                                       SSH_PASSWORD,
                                                                                                       SSH_CMD + ' ' + proj_id + ' ' + proj_name + ' ' + proj_tag + ' ' + str(
                                                                                                           max_id + 1),
                                                                                                       unit, proj_name,
                                                                                                       proj_id,
                                                                                                       proj_tag,
                                                                                                       deploy_status))()
                else:
                    (group(UpdateCurrent.s(sn, status, flow_id, assignee_username, next_assignee_username),
                           UpdateHistoryProcess.s(sn, title,
                                                  sponsor, type_id, content, status, business_id, flow_id,
                                                  assignee_username,
                                                  next_assignee_username, memo, suggest, suggest_content, proj_name,
                                                  proj_tag,
                                                  proj_id)
                           ) | workflow_send_email.si(sn, username, email))()
        if suggest == '拒绝':
            suggest_content = suggest_reject
            status = '已完成'
            next_assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i])
            next_assignee_username = next_assignee.values('username')[0]['username']
            next_assignee_email = next_assignee.values('email')[0]['email']
            username = sponsor_username
            email = sponsor_email
            (group(UpdateCurrent.s(sn, status, flow_id, assignee_username, next_assignee_username),
                   UpdateHistoryProcess.s(sn, title,
                                          sponsor, type_id, content, status, business_id, flow_id, assignee_username,
                                          next_assignee_username, memo, suggest, suggest_content, proj_name, proj_tag,
                                          proj_id)
                   ) | workflow_send_email.si(sn, username, email))()

        '''
        (group(UpdateCurrent.s(sn, status, flow_id, assignee_username,next_assignee_username), UpdateHistoryProcess.s(sn,title,
               sponsor, type_id,content, status,business_id, flow_id,assignee_username,next_assignee_username,memo,suggest,suggest_content,proj_name,proj_tag,proj_id)
               ) | workflow_send_email.si(sn,username,email) )()
        '''

        break


# 手动发布
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def ssh_remote_exec_cmd(self, ip, port, username, password, cmd):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.read().decode()
    # print(lines,type(lines))

    while True:
        # nextline = remote_file.readline().strip()
        nextline = stdout.readline().strip()
        # print(nextline)
        num = 0
        # 遍历任务失败日志
        if "failed=" in nextline:
            num += nextline.split('failed=')[1]
        # 判断任务状态
        if not nextline:
            if "返回值:" in lines:
                if num > 0:
                    task_status = '失败'
                else:
                    task_status = '成功'
            else:
                task_status = '失败'
            # 将任务日志和任务状态写入数据库
            models.deploy_list_detail.objects.filter(task_id=self.request.id).update(status=task_status, )
            break

    ssh.close()
    # 返回result到celery result,并返回task_id
    # return result
    # 不返回result到celery result，仅返回task_id
    return


'''
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def create_task_list_detail(self, unit, proj_name, proj_id, proj_tag, deploy_status, ):
    # print(self.request.id)
    models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                             tag=proj_tag, task_id=self.request.id, status=deploy_status)
'''


# 自动发布
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def ssh_remote_exec_cmd_wf(self, ip, port, username, password, cmd, unit, proj_name, proj_id, proj_tag, deploy_status):
    models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                             tag=proj_tag, task_id=self.request.id, status=deploy_status)

    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.read().decode()
    # print(lines,type(lines))

    while True:
        # nextline = remote_file.readline().strip()
        nextline = stdout.readline().strip()
        # print(nextline)
        num = 0
        # 遍历任务失败日志
        if "failed=" in nextline:
            num += nextline.split('failed=')[1]
        # 判断任务状态
        if not nextline:
            if "返回值:" in lines:
                if num > 0:
                    task_status = '失败'
                else:
                    task_status = '成功'
            else:
                task_status = '失败'
            # 将任务日志和任务状态写入数据库
            models.deploy_list_detail.objects.filter(task_id=self.request.id).update(status=task_status, )
            break

    ssh.close()
    # 返回result到celery result,并返回task_id
    # return result
    # 不返回result到celery result，仅返回task_id
    return


# 手动撤销发布
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def ssh_remote_cancel_exec_cmd(self, ip, port, username, password, cmd):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd)
    ssh.close()
    # 返回result到celery result,并返回task_id
    # return result
    # 不返回result到celery result，仅返回task_id
    return
