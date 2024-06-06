#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from __future__ import absolute_import, unicode_literals

import datetime
import time
import logging

from celery import shared_task, current_app
from celery import signature
from celery.app.control import Control
from celery.worker.control import revoke

# Create your tasks here

from django.core.mail import send_mail
from django.db import DatabaseError, transaction
from django.template import loader, RequestContext
from apps.myapp import token_helper, config_helper, ansible_helper, logger_helper, notify_helper
from django.utils.safestring import mark_safe
from django.core.cache import cache
import json
from django.shortcuts import render
from apps.myapp import models
from django.shortcuts import render_to_response
from django.utils import timezone
import paramiko
import logging
from django.shortcuts import redirect
from celery import group, chain, chord
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from apps.myapp import consumers
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import pickle

from apps.myapp.download_helper import ProjectDownloader
from myweb.celery import app
from myweb.settings import *
from celery.result import AsyncResult


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 30, 'countdown': 60})
def account_send_email(email, username):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)

    title = ACTIVE_EMAIL_SUBJECT
    msg = ''
    send_from = EMAIL_SEND_FROM
    send_to = [email, ]
    fail_silently = False
    token = token_helper.get_random_uuid()

    logger.info(f"Starting account_send_email task with parameters - email: {email}, username: {username}")

    try:
        # 加载和渲染模板
        template = loader.get_template('account/email.html')
        html_str = template.render({"username": username, 'token': token, 'external_url': EXTERNAL_URL})

        # 发送邮件
        send_mail(
            subject=title,
            message=msg,
            from_email=send_from,
            recipient_list=send_to,
            fail_silently=fail_silently,
            html_message=html_str
        )

        logger.info(f"Email successfully sent to {email} for username: {username}")

        # 缓存 token 和 email
        # 记录 token 对应的邮箱是谁 v  k
        cache.set(token, email, 600)
        logger.info(f"Token cached for email: {email}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while sending email to {email} for username: {username} - {e}")
        raise

    finally:
        logger.info(f"Finished account_send_email task for email: {email}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def account_send_email_code(email, verify_code):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)

    title = VERIFY_CODE_EMAIL_SUBJECT
    msg = ''
    send_from = EMAIL_SEND_FROM
    send_to = [email, ]
    fail_silently = False

    logger.info(f"Starting account_send_email_code task with parameters - email: {email}, verify_code: {verify_code}")

    try:
        # 加载和渲染模板
        template = loader.get_template('account/email_code.html')
        html_str = template.render({'verify_code': verify_code})

        # 发送邮件
        send_mail(
            subject=title,
            message=msg,
            from_email=send_from,
            recipient_list=send_to,
            fail_silently=fail_silently,
            html_message=html_str
        )

        logger.info(f"Verification code email successfully sent to {email}")

        # 缓存 verify_code 和 email
        cache.set(verify_code, email, 600)
        logger.info(f"Verification code cached for email: {email}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while sending verification code email to {email} - {e}")
        raise

    finally:
        logger.info(f"Finished account_send_email_code task for email: {email}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_send_email(sn, username, email):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)

    title = WF_EMAIL_SUBJECT
    msg = ''
    send_from = EMAIL_SEND_FROM
    send_to = [email, ]
    fail_silently = False

    logger.info(f"Starting workflow_send_email task with parameters - sn: {sn}, username: {username}, email: {email}")

    try:
        template = loader.get_template('workflow/workflow_email.html')
        html_str = template.render({"username": username, 'sn': sn, 'external_url': EXTERNAL_URL})

        send_mail(
            subject=title,
            message=msg,
            from_email=send_from,
            recipient_list=send_to,
            fail_silently=fail_silently,
            html_message=html_str
        )

        logger.info(f"Email successfully sent to {email} for sn: {sn}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while sending email to {email} for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_send_email task with sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_end_send_email(sn, username, email):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)

    title = WF_EMAIL_SUBJECT
    msg = ''
    send_from = EMAIL_SEND_FROM
    send_to = [email, ]
    fail_silently = False

    logger.info(
        f"Starting workflow_end_send_email task with parameters - sn: {sn}, username: {username}, email: {email}")

    try:
        template = loader.get_template('workflow/workflow_end_email.html')
        html_str = template.render({"username": username, 'sn': sn, 'external_url': EXTERNAL_URL})

        send_mail(
            subject=title,
            message=msg,
            from_email=send_from,
            recipient_list=send_to,
            fail_silently=fail_silently,
            html_message=html_str
        )

        logger.info(f"Email successfully sent to {email} for sn: {sn}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while sending email to {email} for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_end_send_email task with sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_delete_history_process(sn):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)
    logger.info(f"Starting workflow_delete_history_process task with sn: {sn}")

    try:
        with transaction.atomic():
            # 尝试删除记录
            deleted_count, _ = models.wf_info_process_history.objects.filter(sn=sn).delete()
            if deleted_count == 0:
                logger.warning(f"No records were deleted for sn: {sn}")
            else:
                logger.info(f"Successfully deleted {deleted_count} wf_info_process_history records for sn: {sn}")

    except DatabaseError as e:
        # 捕捉数据库错误并记录
        logger.error(f"Database error occurred while deleting wf_info_process_history for sn: {sn} - {e}")
        raise

    except Exception as e:
        # 捕捉所有其他异常并记录
        logger.error(f"An unexpected error occurred while deleting wf_info_process_history for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_delete_history_process task with sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_update_current(sn, status, flow_id, assignee, next_assignee):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)
    logger.info(
        f"Starting workflow_update_current task with parameters - sn: {sn}, status: {status}, flow_id: {flow_id}, "
        f"assignee: {assignee}, next_assignee: {next_assignee}")

    update_time = timezone.now()

    try:
        '''
        使用
        transaction.atomic()
        确保数据库更新操作的原子性，即要么所有的更新操作都成功，要么所有的操作都回滚。
        '''
        with transaction.atomic():
            # 尝试更新记录
            updated_count = models.wf_info.objects.filter(sn=sn).update(
                status=status,
                update_time=update_time,
                flow_id=flow_id,
                next_assignee=next_assignee,
                assignee=assignee
            )
            if updated_count == 0:
                logger.warning(f"No records were updated for sn: {sn}")
            else:
                logger.info(f"Successfully updated wf_info record for sn: {sn}")

    except DatabaseError as e:
        # 捕捉数据库错误并记录
        logger.error(f"Database error occurred while updating wf_info for sn: {sn} - {e}")
        raise

    except Exception as e:
        # 捕捉所有其他异常并记录
        logger.error(f"An unexpected error occurred while updating wf_info for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_update_current task with sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_update_history_process(sn, title, sponsor, type_id, content, status, business_id, flow_id, assignee,
                                    next_assignee, memo, suggest, suggest_content, proj_name, proj_tag, proj_id):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)
    logger.info(f"Starting workflow_update_history_process task")
    try:
        with transaction.atomic():
            # 尝试创建记录
            models.wf_info_process_history.objects.create(
                sn=sn,
                title=title,
                sponsor=sponsor,
                type_id=type_id,
                content=content,
                status=status,
                business_id=business_id,
                flow_id=flow_id,
                assignee=assignee,
                next_assignee=next_assignee,
                memo=memo,
                suggest=suggest,
                suggest_content=suggest_content,
                proj_name=proj_name,
                proj_tag=proj_tag,
                proj_id=proj_id
            )
            logger.info(f"Successfully created wf_info_process_history record for sn: {sn}")

    except DatabaseError as e:
        # 捕捉数据库错误并记录
        logger.error(f"Database error occurred while creating wf_info_process_history for sn: {sn} - {e}")
        raise

    except Exception as e:
        # 捕捉所有其他异常并记录
        logger.error(f"An unexpected error occurred while creating wf_info_process_history for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_update_history_process task with sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_commit(sn):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)
    logger.info(f"Starting workflow_commit task for sn: {sn}")

    try:
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
        next_assignee_username = \
            models.userInfo.objects.filter(workflow_order=order_list_sorted[0]).values('username')[0][
                'username']
        next_assignee_email = models.userInfo.objects.filter(workflow_order=order_list_sorted[0]).values('email')[0][
            'email']
        print(order_list_sorted[0], next_assignee_username, next_assignee_email, order_list_sorted, )
        memo = wf_info.values('memo')[0]['memo']
        suggest = None
        suggest_content = None

        update_current_task = workflow_update_current.si(sn, status, flow_id, assignee_username, next_assignee_username)
        update_history_task = workflow_update_history_process.si(
            sn, title, sponsor, type_id, content, status, business_id, flow_id,
            assignee_username, next_assignee_username, memo, suggest, suggest_content, proj_name, proj_tag, proj_id
        )
        send_email_task = workflow_send_email.si(sn, next_assignee_username, next_assignee_email)

        parallel_tasks = group(update_current_task,
                               update_history_task,
                               )

        workflow_chain = chain(parallel_tasks,
                               send_email_task)
        workflow_chain.apply_async()

        logger.info(f"Workflow commit process completed for sn: {sn}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while processing workflow commit for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_commit task for sn: {sn}")


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_withdraw(sn):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)

    status = '未提交'
    flow_id = -1
    assignee_username = ''
    next_assignee_username = ''

    try:
        # 创建任务链并将其应用异步执行
        chain(
            workflow_delete_history_process.si(sn),
            workflow_update_current.si(sn, status, flow_id, assignee_username, next_assignee_username)
        ).apply_async()

        logger.info(f"Workflow withdrawal process completed for sn: {sn}")

    except Exception as e:
        # 捕捉所有异常并记录
        logger.error(f"An error occurred while processing workflow withdrawal for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_withdraw task for sn: {sn}")
    (workflow_delete_history_process.s(sn) | workflow_update_current.si(sn, status, flow_id, assignee_username,
                                                                        next_assignee_username)
     )()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 3})
def workflow_process(sn, suggest, suggest_agree, suggest_reject, ):
    # 获取当前模块命名的记录器
    logger = logging.getLogger(__name__)
    logger.info(f"Starting workflow_process task for sn: {sn}")

    try:
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
        # 2024/6/5
        qs_asset = models.Asset.objects.filter(business_unit_id=business_id)
        # 通过value_list 获取ansible_vars外键中的字段
        host_list = list(qs_asset.values_list('ip', 'ansible_vars__vars'))
        print(host_list)
        tomcat_job = TOMCAT_JOB_LIST

        memo = wf_info.values('memo')[0]['memo']

        # 2023/08/17
        proj_name = wf_info.values('proj_name')[0]['proj_name']
        proj_tag = wf_info.values('proj_tag')[0]['proj_tag']
        proj_id = wf_info.values('proj_id')[0]['proj_id']
        unit = models.wf_business.objects.filter(id=business_id).values('name')[0]['name']
        deploy_status = '执行中'
        try:
            max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
        except AttributeError:
            # 如果数据库为空，则返回0:
            max_id = 0
        print(max_id, type(max_id))

        # 2024/6/5
        log_dir = os.path.join(ANSIBLE_BASE_DIR, 'logs')  # 设置日志目录
        log_file_path = os.path.join(log_dir, f"ansible_deploy-{max_id + 1}.log")
        if proj_name in tomcat_job:
            job_name = "build_java_prod"
        else:
            job_name = "build_java"

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
                    (group(workflow_update_current.s(sn, status, flow_id, assignee_username, next_assignee_username),
                           workflow_update_history_process.s(sn, title, sponsor, type_id, content, status, business_id,
                                                             flow_id, assignee_username, next_assignee_username, memo,
                                                             suggest, suggest_content, proj_name, proj_tag, proj_id)
                           ) | workflow_send_email.si(sn, username, email)
                     )()
                else:
                    status = '已完成'
                    next_assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i])
                    next_assignee_username = next_assignee.values('username')[0]['username']
                    next_assignee_email = next_assignee.values('email')[0]['email']
                    username = sponsor_username
                    email = sponsor_email
                    # 判断工单类型是否‘生产发布’
                    if proj_name:
                        # Create a group to run `workflow_update_current` and `workflow_update_history_process` in parallel
                        parallel_tasks = group(
                            workflow_update_current.s(sn, status, flow_id, assignee_username, next_assignee_username),
                            workflow_update_history_process.s(sn, title, sponsor, type_id, content, status, business_id,
                                                              flow_id, assignee_username, next_assignee_username, memo,
                                                              suggest, suggest_content, proj_name, proj_tag, proj_id)
                        )

                        # Chain the group with `workflow_end_send_email、deploy_add_deploy_list_detail、deploy_deploy` to
                        # run it after the parallel tasks complete
                        workflow_chain = chain(
                            parallel_tasks,
                            workflow_end_send_email.si(sn, username, email),
                            deploy_add_deploy_list_detail.si(unit, proj_name, proj_id, proj_tag, deploy_status),
                            deploy_main.si(unit, host_list, GITLAB_URL, {"PRIVATE-TOKEN": GITLAB_TOKEN, },
                                           os.path.join(ANSIBLE_BASE_DIR, 'temp_download'),
                                           os.path.join(ANSIBLE_BASE_DIR, 'temp_unzip'),
                                           os.path.join(ANSIBLE_BASE_DIR, 'roles'),
                                           proj_name, proj_id, proj_tag, job_name,
                                           os.path.join(ANSIBLE_BASE_DIR, 'inventory', f'{unit}.ini'),
                                           os.path.join(ANSIBLE_BASE_DIR, f'{proj_name}.yml'),
                                           str(max_id + 1), log_file_path)
                        )

                        # Run the task chain
                        task_result = workflow_chain.apply_async()
                    else:
                        # Create a group to run `workflow_update_current` and `workflow_update_history_process` in parallel
                        parallel_tasks = group(
                            workflow_update_current.s(sn, status, flow_id, assignee_username, next_assignee_username),
                            workflow_update_history_process.s(sn, title, sponsor, type_id, content, status, business_id,
                                                              flow_id, assignee_username, next_assignee_username, memo,
                                                              suggest, suggest_content, proj_name, proj_tag, proj_id)
                        )

                        # Chain the group with `workflow_end_send_email` to run it after the parallel tasks complete
                        workflow_chain = chain(
                            parallel_tasks,
                            workflow_end_send_email.si(sn, username, email),
                        )

                        # Run the task chain
                        task_result = workflow_chain.apply_async()

            if suggest == '拒绝':
                suggest_content = suggest_reject
                status = '已完成'
                next_assignee = models.userInfo.objects.filter(workflow_order=order_list_sorted[i])
                next_assignee_username = next_assignee.values('username')[0]['username']
                next_assignee_email = next_assignee.values('email')[0]['email']
                username = sponsor_username
                email = sponsor_email

                # Create a group to run `workflow_update_current` and `workflow_update_history_process` in parallel
                parallel_tasks = group(
                    workflow_update_current.s(sn, status, flow_id, assignee_username, next_assignee_username),
                    workflow_update_history_process.s(sn, title, sponsor, type_id, content, status, business_id,
                                                      flow_id, assignee_username, next_assignee_username, memo,
                                                      suggest, suggest_content, proj_name, proj_tag, proj_id)
                )

                # Chain the group with `workflow_end_send_email` to run it after the parallel tasks complete
                workflow_chain = chain(
                    parallel_tasks,
                    workflow_end_send_email.si(sn, username, email),
                )

                # Run the task chain
                task_result = workflow_chain.apply_async()

            break
    except Exception as e:
        logger.error(f"An error occurred while processing workflow process for sn: {sn} - {e}")
        raise

    finally:
        logger.info(f"Finished workflow_process task for sn: {sn}")


# 手动发布
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def deploy_ssh_remote_exec_cmd(self, ip, port, username, password, cmd):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.read().decode()
    # print(lines,type(lines))

    num = 0

    # 遍历任务失败日志
    for item in lines.split('\n'):
        if "failed=" in item:
            # print (nextline.split('failed=')[1], type(nextline.split('failed=')[1]))
            num += int(item.strip().split('failed=')[1])
            # print (num)
        if "返回值：" in item:
            num += int(item.strip().split('返回值：')[1])
        if "下载失败" in item:
            num += 1
        if "ERROR:" in item:
            num += 1

    # 判断任务状态
    if num > 0:
        task_status = '失败'
    else:
        task_status = '成功'
    # print(task_status)
    # print(num)
    # 将任务日志和任务状态写入数据库
    models.deploy_list_detail.objects.filter(task_id=self.request.id).update(status=task_status, )

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
def deploy_wf_ssh_remote_exec_cmd(self, ip, port, username, password, cmd, unit, proj_name, proj_id, proj_tag,
                                  deploy_status):
    models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                             tag=proj_tag, task_id=self.request.id, status=deploy_status)

    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.read().decode()
    # print(lines,type(lines))

    num = 0

    # 遍历任务失败日志
    for item in lines.split('\n'):
        if "failed=" in item:
            # print (nextline.split('failed=')[1], type(nextline.split('failed=')[1]))
            num += int(item.strip().split('failed=')[1])
            # print (num)
        if "返回值：" in item:
            num += int(item.strip().split('返回值：')[1])
        if "下载失败" in item:
            num += 1
        if "ERROR:" in item:
            num += 1

    # 判断任务状态
    if num > 0:
        task_status = '失败'
    else:
        task_status = '成功'
    # print(task_status)
    # print(num)
    # 将任务日志和任务状态写入数据库
    models.deploy_list_detail.objects.filter(task_id=self.request.id).update(status=task_status, )

    ssh.close()
    # 返回result到celery result,并返回task_id
    # return result
    # 不返回result到celery result，仅返回task_id
    return


# 手动撤销发布
# @shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10}, )
@shared_task(bind=True)
def deploy_cancel_ssh_remote_exec_cmd(self, ip, port, username, password, cmd):
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


@shared_task(bind=True)
def deploy_add_deploy_list_detail(self, unit, proj_name, proj_id, proj_tag, deploy_status):
    # 配置日志记录器
    logger = logging.getLogger(__name__)
    logger.info(f"Starting deploy_add_deploy_list_detail task with ID: {self.request.id}")
    try:
        # 尝试创建记录
        models.deploy_list_detail.objects.create(
            unit=unit,
            proj_name=proj_name,
            proj_id=proj_id,
            tag=proj_tag,
            task_id=self.request.id,
            status=deploy_status
        )
        logger.info(f"Successfully created deploy_list_detail record for task ID: {self.request.id}")

    except DatabaseError as e:
        # 捕捉数据库错误并记录
        logger.error(f"Database error occurred for task ID: {self.request.id} - {e}")
        # 可以根据需要抛出自定义异常或执行其他操作
        raise

    except Exception as e:
        # 捕捉所有其他异常并记录
        logger.error(f"An unexpected error occurred for task ID: {self.request.id} - {e}")
        # 可以根据需要抛出自定义异常或执行其他操作
        raise

    finally:
        logger.info(f"Finished deploy_add_deploy_list_detail task with ID: {self.request.id}")


@shared_task(bind=True)
def deploy_generate_config(self, unit, host_list, deploy_id):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()  # 重定向标准输出和标准错误

    # 创建 CustomConfigParser 对象
    config = config_helper.CustomConfigParser()

    # Example dynamic input: sections and their entries
    '''
    sections = {
        'default': [
            ('192.168.13.39', 'ansible_ssh_user=root ansible_ssh_pass=redhat'),
            ('10.13.13.63', 'ansible_ssh_user=root ansible_ssh_pass=redhat'),
            ('10.13.13.67', None)
        ],
        'foo': [
            ('10.8.9.11', 'ansible_ssh_user=root ansible_ssh_pass=redhat'),
            ('10.8.9.12', 'ansible_ssh_user=root ansible_ssh_pass=redhat'),
            ('10.8.9.13', None)
        ]
    }
    '''
    sections = {
        unit: host_list
    }

    # Add sections and their entries to the config
    for section, hosts in sections.items():
        config.add_section(section)
        for host, config_data in hosts:
            # print(host, config_data)
            if config_data:
                # Combine host and its configuration
                full_entry = f"{host} {config_data}"
                # print(full_entry, '1')
            else:
                # Only use the host if there's no additional configuration
                full_entry = host
                # print(full_entry, '0')
            # We use full_entry as both the key and value since it's the full line in the required format
            config.set(section, full_entry, full_entry)

    # 判断配置目录是否存在
    inventory_dir = os.path.join(ANSIBLE_BASE_DIR, 'inventory')
    if not os.path.exists(inventory_dir):
        os.makedirs(inventory_dir)

    inventory_file = os.path.join(inventory_dir, f'{unit}.ini')

    try:
        # 将配置写入文件
        with open(inventory_file, 'w') as configfile:
            config.write(configfile)
        # 记录信息
        result = f"Ansible playbook 主机配置文件 '{inventory_file}' 生成完成"
        logger.info(result)

        # 更新发布的当前阶段task_id
        # models.deploy_list_detail.objects.filter(id=deploy_id).update(task_id=self.request.id)
        # 记录信息
        logger.info(f"阶段 deploy_generate_config 完成，任务id： '{self.request.id}'")

    except Exception as e:
        # 记录信息
        logger.error(f"An error occurred: {e}")
        # 更新任务状态
        models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")
        result = str(e)

    # 返回任务ID
    return {'deploy_id': deploy_id, 'stage': 'deploy_generate_config', 'result': result}


@shared_task(bind=True)
def deploy_download_artifact(self, host, headers, download_dir, unzip_dir, deploy_dir, pkg_name, project_id,
                             project_tag, job_name, deploy_id):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()  # 重定向标准输出和标准错误
    try:
        # logging.info('Starting download artifact task')
        logger.info('Starting download artifact task')

        downloader = ProjectDownloader(host, headers, download_dir, unzip_dir, deploy_dir, pkg_name, project_id,
                                       project_tag, job_name)
        artifact = downloader.download_project_artifact()
        if artifact:
            downloader.unzip_project_artifact(artifact)
            sub_dirs = downloader.get_sub_dirs(unzip_dir, [])
            # print(sub_dirs)
            if sub_dirs:
                first_sub_dir = sub_dirs[0]
                # print(first_sub_dir)
                # linux
                downloader.bak(os.path.join(deploy_dir, pkg_name, "files", first_sub_dir.split('/')[-1]))
                # windows: "\\" ,需要转义； join方法不要使用"/files/"，应该为"files"
                # downloader.bak(os.path.join(deploy_dir, pkg_name, "files", first_sub_dir.split('\\')[-1]))
                downloader.publish(first_sub_dir)
            downloader.clean(download_dir)
            downloader.clean(unzip_dir)
            result = 'Artifact 下载及备份处理完成'
            logger.info(result)

            # 更新发布的当前阶段task_id
            # models.deploy_list_detail.objects.filter(id=deploy_id).update(task_id=self.request.id)
            # 记录信息
            logger.info(f"阶段 deploy_download_artifact 完成，任务id： '{self.request.id}'")
        else:
            logger.error('No artifact found')
            # 更新任务状态
            models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # 更新任务状态
        models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")
        result = str(e)

    # 返回任务ID
    return {'deploy_id': deploy_id, 'stage': 'deploy_download_artifact', 'result': result}


def deploy_notify(host_status_count, deploy_id, playbooks):
    # 以主机维度统计各个状态值（简化状态显示，用“成功/失败”表示）
    host_statuses = {}
    failed_or_unreachable_count = 0

    for host, status in host_status_count.items():
        if status["failed"] > 0 or status["unreachable"] > 0:
            host_statuses[host] = "失败"
            failed_or_unreachable_count += 1
        else:
            host_statuses[host] = "成功"

    overall_status = "失败" if failed_or_unreachable_count > 0 else "成功"

    # 格式化输出消息
    status = overall_status
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host_statuses_json = json.dumps(host_statuses, indent=4, ensure_ascii=False)

    msg = (
        f"服务名称：{playbooks}\n\n"
        f"执行结果：{status}\n\n"
        f"发布时间：{current_time}\n\n"
        f"发布详情：\n{host_statuses_json}"
    )

    print(msg)

    # 发送通知
    alert_sender = notify_helper.AlertSender()
    alert_sender.send_welkin(DEPLOY_WELINK_WEBHOOK_URL, DEPLOY_WELINK_UUID, msg)

    return {'deploy_id': deploy_id, 'stage': 'deploy_notify', 'host_statuses': host_statuses}


@shared_task(bind=True, soft_time_limit=300, time_limit=600)  # 5 minutes soft limit, 10 minutes hard limit
def deploy_ansible_playbook(self, host_file, playbooks, deploy_id):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()  # 重定向标准输出和标准错误

    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'False'
    os.environ['ANSIBLE_VERBOSITY'] = '1'
    '''
    0: Default level, minimal output.
    1: Basic debugging, more information about the executed tasks.
    2: More detailed debugging, including tasks' details.
    3: Detailed information, including task start and end.
    4: Full debug, including detailed internal execution steps.
    '''

    inventory_path = os.path.join(ANSIBLE_BASE_DIR, 'inventory', host_file)

    '''
    # Create a temporary ansible.cfg file
    with open('ansible.cfg', 'w') as configfile:
        configfile.write(f'[defaults]\nhost_key_checking = False\ninventory = {inventory_dir}\n')
    '''
    # logging.info(f"Running Ansible playbook: {playbooks} with host file: {host_file}")
    logger.info(f"Running Ansible playbook: {playbooks} with host file: {host_file}")

    try:
        playbooks = [playbooks]
        ansible_runner = ansible_helper.AnsibleRunner(inventory_path)
        ansible_runner.run_playbook(playbooks)
        ansible_runner.print_results()
        result = ansible_runner.get_result()

        # 记录发布结果汇总
        logger.info(f"Ansible playbook {playbooks} 执行完成")
        logger.info(f"Ansible Playbook 执行统计：************** {result}")

        # 更新发布的当前阶段task_id
        # models.deploy_list_detail.objects.filter(id=deploy_id).update(task_id=self.request.id)

        # 判断整体任务状态并发送通知
        notify_result = deploy_notify(result, deploy_id, playbooks)
        logger.info(f"通知结果: {notify_result}")

        logger.info(f"阶段 deploy_ansible_playbook 完成，任务id： '{self.request.id}'")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # 更新任务状态
        models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")
        result = str(e)

    finally:
        # os.remove('ansible.cfg')
        logger.info(f"deploy_id {deploy_id} 结束----------------------")

    # 返回任务ID
    # return self.request.id
    return {'deploy_id': deploy_id, 'stage': 'deploy_ansible_playbook', 'result': result}


@shared_task(bind=True)
def deploy_stat(self, deploy_id, log_file_path):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()  # 重定向标准输出和标准错误
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            start_reading = False
            log_lines = []
            num = 0

            # 读取日志文件并提取相关内容
            for line in log_file:
                if start_reading:
                    log_lines.append(line)
                    if line.strip().endswith(f"deploy_id {deploy_id} 结束----------------------"):
                        break
                elif line.strip().endswith(f"deploy_id {deploy_id} 开始----------------------"):
                    start_reading = True
                    log_lines.append(line)

            # print(log_lines)

            # 分析提取的日志行
            if start_reading:
                for item in log_lines:
                    if "Failed:" in item:
                        num += int(item.split('Failed:')[1].strip())
                    if "Down:" in item:
                        num += int(item.split('Down:')[1].strip())
                    if "An error occurred:" in item:
                        num += 1
                    if "No artifact found" in item:
                        num += 1

                task_status = '失败' if num > 0 else '成功'
                # print(task_status)
                # print(num)

                # 更新发布的当前阶段task_id
                # models.deploy_list_detail.objects.filter(id=deploy_id).update(task_id=self.request.id)
                # 记录信息
                logger.info(f"发布状态统计 for deploy_id {deploy_id}: {task_status}")
                logger.info(f"发布错误数量 for deploy_id {deploy_id}: {num}")
                logger.info(f"阶段 deploy_stat 完成，任务id： '{self.request.id}'")
            else:
                # print(f"未找到开始标志 deploy_id {deploy_id} 开始----------------------")
                logger.error(f"未找到开始标志 deploy_id {deploy_id} 开始----------------------")
                # 更新任务状态
                models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")

    except FileNotFoundError:
        # print(f"文件未找到: {log_file_path}")
        logger.error(f"文件未找到: {log_file_path}")
        # 更新任务状态
        models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")
    except Exception as e:
        # print(f"发生错误: {e}")
        logger.error(f"发生错误: {e}")
        # 更新任务状态
        models.deploy_list_detail.objects.filter(id=deploy_id).update(status="失败")

    # return self.request.id
    return {'deploy_id': deploy_id, 'stage': 'deploy_stat', 'log_lines': log_lines, 'task_status': task_status}


@shared_task(bind=True)
def deploy_main(self, unit, host_list, host, headers, download_dir, unzip_dir, deploy_dir, pkg_name, project_id,
                project_tag, job_name, host_file, playbooks, deploy_id, log_file_path):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()  # 重定向标准输出和标准错误

    # logging.info(f"deploy_id {deploy_id} 开始----------------------")
    logger.info(f"deploy_id {deploy_id} 开始----------------------")

    # Create a group to run `deploy_generate_config` and `deploy_download_artifact` in parallel
    parallel_tasks = group(
        deploy_generate_config.si(unit, host_list, deploy_id),  # Immutable signature
        deploy_download_artifact.si(host, headers, download_dir, unzip_dir, deploy_dir, pkg_name, project_id,
                                    project_tag, job_name, deploy_id)  # Immutable signature
    )

    # Chain the group with `deploy_ansible_playbook` to run it after the parallel tasks complete
    deployment_chain = chain(
        parallel_tasks,
        deploy_ansible_playbook.si(host_file, playbooks, deploy_id),  # Immutable signature
        deploy_stat.si(deploy_id, log_file_path)
    )

    # Run the task chain
    task_result = deployment_chain.apply_async()

    # Wait for the task chain to complete
    while not task_result.ready():  # Check if the task is not yet ready
        time.sleep(1)  # Wait for 1 second before checking again

    # 任务结果的元数据
    result_meta = task_result._get_task_meta()
    # print(result_meta)
    # logger.info(result_meta)
    task_status = result_meta['result'].get('task_status')
    task_log = result_meta['result'].get('log_lines')

    # 将任务日志和任务状态写入数据库
    '''
    models.deploy_list_detail.objects.filter(task_id=self.request.id).update(
        status=task_status,
        # task_log='\n'.join(task_log)  # 将日志列表转换为单个字符串
        task_log=''.join(task_log)  # 将日志列表转换为单个字符串
    )
    '''
    # 判断任务是否被取消
    current_status = models.deploy_list_detail.objects.filter(id=deploy_id).first().status
    if current_status == "已取消":
        models.deploy_list_detail.objects.filter(id=deploy_id).update(
            # task_log='\n'.join(task_log)  # 将日志列表转换为单个字符串
            task_log=''.join(task_log)  # 将日志列表转换为单个字符串
        )
    elif current_status == "执行中":
        models.deploy_list_detail.objects.filter(id=deploy_id).update(
            status=task_status,
            # task_log='\n'.join(task_log)  # 将日志列表转换为单个字符串
            task_log=''.join(task_log)  # 将日志列表转换为单个字符串
        )
    result = f"发布任务全部执行完成"

    # return task_result.id
    return {'deploy_id': deploy_id, 'stage': 'deploy_deploy', 'result': result}


# celery revoke未成功，暂时不可用
@shared_task(bind=True, soft_time_limit=30, time_limit=60)
def deploy_cancel(self, deploy_id, task_id):
    # 配置 logger
    logger_setup = logger_helper.LoggerSetup(f"ansible_deploy-{deploy_id}.log", os.path.join(ANSIBLE_BASE_DIR, 'logs'))
    logger = logger_setup.get_logger()
    logger_setup.redirect_std_output()
    """
    celery_control = Control(app=app)
    def revoke_task(parent_task_id):
        result = AsyncResult(task_id)
        if result:
            # Revoke the main task
            celery_control.revoke(parent_task_id, terminate=True, signal='KILL')
            # Poll for the task to be ready
            while not result.ready():
                time.sleep(1)  # Wait for 1 second before checking again
            # Revoke all subtasks if any
            if result.children:
                for child in result.children:
                    revoke_task(child.id)

    # Start revoking from the root task
    revoke_task(task_id)
    """

    def extract_child_task_ids(task_result):
        """
        递归提取所有子任务的 task_id
        """
        task_ids = []
        if not task_result:
            return task_ids

        if isinstance(task_result, list):
            for item in task_result:
                task_ids.extend(extract_child_task_ids(item))
        elif isinstance(task_result, tuple):
            for item in task_result:
                task_ids.extend(extract_child_task_ids(item))
        elif isinstance(task_result, AsyncResult):
            task_ids.append(task_result.id)
            if task_result.children:
                for child in task_result.children:
                    task_ids.extend(extract_child_task_ids(child))
        return task_ids

    def revoke_chain(result):
        if result:
            result.revoke()
            # result = result.parent

            if extract_child_task_ids(result):
                for child in extract_child_task_ids(result):
                    print(child)
                    revoke_chain(AsyncResult(child))

    task = AsyncResult(task_id)
    revoke_chain(task)

    logger.info(f"All tasks related to deploy_id {deploy_id} have been revoked.")

    return f"All tasks related to deploy_id {deploy_id} have been revoked."
