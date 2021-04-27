#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import signature

# Create your tasks here

from django.core.mail import send_mail
from django.template import loader,RequestContext
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


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 30, 'countdown': 60})
def send_email(email,username):
    title = '【CMDB激活邮件】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email,]
    fail_silently = False
    token = token_helper.get_random_uuid()
    # 加载模板
    template = loader.get_template('backend/email.html')
    # 渲染模板
    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
    html_str = template.render({"username": username, 'token': token, })
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    send_mail(title, msg, send_from, send_to, fail_silently, html_message = html_str)
    #print(html_str,type(html_str))
    # 记录 token 对应的邮箱是谁 v  k
    cache.set(token, email, 600)
    #print(cache.get(token))


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_email_code(email,verify_code):
    title = '【CMDB找回密码邮件】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email,]
    fail_silently = False
    #verify_code = token_helper.get_random_code()
    # 加载模板
    template = loader.get_template('backend/email_code.html')
    # 渲染模板
    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
    html_str = template.render({'verify_code': verify_code, })
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    send_mail(title, msg, send_from, send_to, fail_silently, html_message = html_str)
    #print(html_str,type(html_str))
    # 记录 token 对应的邮箱是谁 v  k
    cache.set(verify_code, email,600)
    #print(cache.get(verify_code))
    #return (verify_code)

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def workflow_send_email(sn,username,email):
    title = '【流程审批提醒】'
    msg = ''
    send_from = '834163059@qq.com'
    send_to = [email,]
    fail_silently = False
    #token = token_helper.get_random_uuid()
    # 加载模板
    template = loader.get_template('workflow/email_workflow.html')
    # 渲染模板
    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
    html_str = template.render({"username": username, 'sn': sn, })
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    res=send_mail(title, msg, send_from, send_to, fail_silently, html_message = html_str)
    #print(html_str,type(html_str))
    # 记录 token 对应的邮箱是谁 v  k
    #cache.set(token, email, 600)
    #print(cache.get(token))
    #return res


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def workflow_commit(sn):
    wf_info = models.wf_info.objects.filter(sn=sn)
    status = '已提交'
    update_time = timezone.now()
    flow_id = 1
    wf_info.update(status=status, update_time=update_time, flow_id=flow_id)
    approval_selected_id = wf_info.values('approval')[0]['approval']
    approval_selected = models.userInfo.objects.filter(id=approval_selected_id)
    email = approval_selected.values('email')[0]['email']
    username = approval_selected.values('username')[0]['username']
    type_id = wf_info.values('type')[0]['type']
    sponsor = wf_info.values('sponsor')[0]['sponsor']
    title = wf_info.values('title')[0]['title']
    content = wf_info.values('content')[0]['content']
    business_id = wf_info.values('business')[0]['business']
    models.wf_info_history_commit.objects.create(sn=sn, title=title, sponsor=sponsor, type_id=type_id,
        approval_id=approval_selected_id, content=content, status=status, business_id=business_id,flow_id=flow_id)
    return sn

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def workflow_process(sn,title,username_sponsor,type,content,suggest,suggest_agree,assignee,suggest_reject,flow_id):
    wf_info = models.wf_info.objects.filter(sn=sn)
    business_id = wf_info.values('business')[0]['business']
    wf_business = models.wf_business.objects.filter(id=business_id)
    group_id = wf_business.values('group')[0]['group']
    approval = models.userInfo.objects.filter(group_id=group_id).filter(approval='1')
    approval_ins = models.userInfo.objects.filter(group_id=group_id).get(approval='1')
    username_approval = approval.values('username')[0]['username']
    email_approval = approval.values('email')[0]['email']
    type_id = models.wf_type.objects.get(name=type)

    if suggest == '同意':
        if flow_id < 3:
            status = '处理中'
            #flow_id += flow_id  # 每次处理flow_id值加1
            models.wf_info_history_process.objects.create(sn=sn, title=title, sponsor=username_sponsor, type=type_id,
                                                          approval=approval_ins, content=content, suggest=suggest,
                                                          suggest_content=suggest_agree, assignee=assignee,
                                                          business_id=business_id, flow_id=flow_id)
        else:
            status = '已完成'
            models.wf_info_history_process.objects.create(sn=sn, title=title, sponsor=username_sponsor, type=type_id,
                                                          approval=approval_ins, content=content, suggest=suggest,
                                                          suggest_content=suggest_agree, assignee=assignee,
                                                          business_id=business_id, flow_id=flow_id)
            models.wf_info_history_complete.objects.create(sn=sn, title=title, sponsor=username_sponsor, type=type_id,
                                                          content=content, suggest=suggest,
                                                          suggest_content=suggest_agree, assignee=assignee,
                                                          business_id=business_id, flow_id=flow_id)
        update_time = timezone.now()
        #wf_type = models.wf_type.objects.all()
        wf_info.update(status=status, update_time=update_time, approval=approval_ins,flow_id=flow_id )

        return sn

    if suggest == '拒绝':
        status = '已完成'
        update_time = timezone.now()
        finish_time = timezone.now()
        wf_info.update(status=status, update_time=update_time, approval=approval_ins, finish_time=finish_time, flow_id=flow_id)
        models.wf_info_history_process.objects.create(sn=sn, title=title, sponsor=username_sponsor, type=type_id,
                                                      approval=approval_ins, content=content, suggest=suggest,
                                                      suggest_content=suggest_reject, assignee=assignee,
                                                      business_id=business_id, flow_id=flow_id)
        models.wf_info_history_complete.objects.create(sn=sn, title=title, sponsor=username_sponsor, type=type_id,
                                                       content=content, suggest=suggest,
                                                       suggest_content=suggest_reject,assignee=assignee,
                                                       business_id=business_id, flow_id=flow_id)
        return sn


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 30, 'countdown': 60})
def deploy(host,port,username,password,command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read()
    ssh.close()
    #return result


