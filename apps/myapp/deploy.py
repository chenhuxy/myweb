#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime
import re
import signal
import time

from django.db.models.functions import ExtractYear, ExtractMonth

from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import HttpResponse
from apps.myapp import models
from django.shortcuts import redirect
from apps.myapp import tasks, common, page_helper
from apps.myapp import token_helper
from django.utils import timezone
import os, json
from django.http import JsonResponse
from django.core import serializers
from celery import chord, group, chain, current_app
from django.db.models import Q, Count
from apps.myapp.gitlab_helper import GitTools
import gitlab
import paramiko, subprocess
from django.core.cache import cache
from myweb.settings import *
from apps.myapp.paramiko_ssh_helper import ssh_remote
from celery.result import AsyncResult
from celery.app.control import Control
from myweb.celery import app
from myweb import celery_app
from myweb.celery import app
from celery.app.control import Control


@custom_login_required
@custom_permission_required('myapp.view_deploy_script_type')
def deploy_type(request, *args, **kwargs):
    qs_deploy_type = models.DeployType.objects.all()
    count = qs_deploy_type.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'qs_deploy_type': qs_deploy_type, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_script_type')
def deploy_type_form_add(request, *args, **kwargs):
    qs_deploy_type = models.DeployType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'qs_deploy_type': qs_deploy_type, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_script_type')
def deploy_type_form_update(request, *args, **kwargs):
    deploy_type_id = kwargs['id']
    qs_deploy_type = models.DeployType.objects.filter(id=deploy_type_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'login_user': user_dict['user'], 'status': '操作成功', 'id': deploy_type_id,
           'qs_deploy_type': qs_deploy_type, 'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('deploy/deploy_type_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_script_type')
def deploy_type_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        deploy_type_name = request.POST.get('deploy-type', None)
        is_exist = models.DeployType.objects.filter(name=deploy_type_name)
        # print(is_exist)
        if not is_exist:
            is_empty = all([deploy_type_name, ])
            if is_empty:
                models.DeployType.objects.create(name=deploy_type_name, )
                msg = {'deploy_type_name': deploy_type_name, 'login_user': user_dict['user'],
                       'status': '添加发布类型成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/deploy/deploy-type/list/')
            else:
                msg = {'deploy_type_name': deploy_type_name, 'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'deploy_type_name': deploy_type_name, 'login_user': user_dict['user'], 'status': '该发布类型已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_script_type')
def deploy_type_update(request, *args, **kwargs):
    deploy_type_id = kwargs['id']
    deploy_type_name = request.POST.get('deploy-type')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.DeployType.objects.filter(id=deploy_type_id).update(name=deploy_type_name, )
    return redirect('/cmdb/index/deploy/deploy-type/list/')


@custom_login_required
@custom_permission_required('myapp.delete_deploy_script_type')
def deploy_type_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.DeployType.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除发布类型成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('deploy/deploy_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_app')
def deploy_app(request, *args, **kwargs):
    count = models.deploy_app.objects.all().count()
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    deploy = models.deploy_app.objects.all()[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_app_list(request, page, pageinfo.pageCount)
    msg = {'deploy': deploy, 'login_user': user_dict['user'], 'count': count,
           'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_app.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_app')
def deploy_app_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/deploy/app/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/deploy/app/list/')


@custom_login_required
@custom_permission_required('myapp.view_deploy_app')
def deploy_app_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    deploy = models.deploy_app.objects.filter(proj_name__icontains=keyword) | models.deploy_app.objects.filter(
        proj_id__icontains=keyword)
    count = deploy.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    deploy = deploy[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_app_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'deploy': deploy, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('deploy/deploy_app.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_app')
def deploy_app_form_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    business = models.wf_business.objects.all()
    deploy = models.deploy_app.objects.all()
    # usergroup = models.userGroup.objects.all()
    approval = userinfo.exclude(workflow_order=0)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'business': business, 'userinfo': userinfo, 'deploy': deploy,
           'login_user': user_dict['user'], 'status': '', 'approval': approval,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('deploy/deploy_app_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_app')
def deploy_app_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    business = models.wf_business.objects.all()
    if request.method == 'POST':
        unit_id = request.POST.get('unit', None)
        unit = models.wf_business.objects.filter(id=unit_id).values('name')[0]['name']
        proj_name = request.POST.get('proj_name', None)
        proj_id = request.POST.get('proj_id', None)
        is_exist = models.deploy_app.objects.filter(proj_name=proj_name)
        # print(is_exist)
        if not is_exist:
            is_empty = all([proj_id, proj_name, unit])
            if is_empty:
                queryset = models.deploy_app.objects.create(unit_id=unit_id, proj_id=proj_id, proj_name=proj_name, )
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': user_dict['user'], 'status': '添加应用成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/deploy/app/list/')
            else:
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': user_dict['user'], 'status': 'xx不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'userinfo': userinfo, 'business': business,
                   'login_user': user_dict['user'], 'status': '该应用已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_app_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_app')
def deploy_app_form_update(request, *args, **kwargs):
    id = kwargs['id']
    deploy = models.deploy_app.objects.filter(id=id)
    business = models.wf_business.objects.all().exclude(unit__id=id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': id, 'login_user': user_dict['user'], 'status': u'操作成功', 'deploy': deploy, 'business': business,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('deploy/deploy_app_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_app')
def deploy_app_update(request, *args, **kwargs):
    id = kwargs['id']
    unit_id = request.POST.get('unit', None)
    unit = models.wf_business.objects.filter(id=unit_id).values('name')
    # print(unit)
    proj_name = request.POST.get('proj_name', None)
    proj_id = request.POST.get('proj_id', None)
    update_time = timezone.now()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.deploy_app.objects.filter(id=id).update(unit_id=unit_id, proj_id=proj_id, proj_name=proj_name,
                                                   update_time=update_time, )
    return redirect('/cmdb/index/deploy/app/list/')


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def deploy_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            wfbusiness_id = request.POST.get('wfbusiness', None)
            # print(wfbusiness_id)
            wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id)
            director_id = wfbusiness.values('director_id')[0]['director_id']
            director = models.userInfo.objects.filter(id=director_id).values('username')[0]['username']
            # print(wfbusiness, director_id, director, )
            user_dict = request.session.get('is_login', None)
            wf_dict = request.session.get('wf', None)
            # data = serializers.serialize('json',wfbusiness) #序列化
            # data = json.dumps(wfbusiness)
            data = {'director_id': director_id, 'director': director, }
            # print(data)
            # return HttpResponse(json.dumps(data))
        except:
            data = {'director_id': '0', 'director': '------------- 请选择 -------------', }
        finally:
            return HttpResponse(json.dumps(data))


@custom_login_required
@custom_permission_required('myapp.delete_deploy_app')
def deploy_app_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.deploy_app.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除app成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('deploy/deploy_app.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list(request, *args, **kwargs):
    count = models.deploy_list_detail.objects.all().count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    # 发布列表降序排列
    deploy = models.deploy_list_detail.objects.all().order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_task_list(request, page, pageinfo.pageCount)

    msg = {'deploy': deploy, 'login_user': user_dict['user'], 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/deploy_list.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/deploy/task/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/deploy/task/list/')


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    deploy = models.deploy_list_detail.objects.filter(
        proj_name__icontains=keyword) | models.deploy_list_detail.objects.filter(status__icontains=keyword)
    count = deploy.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    deploy = deploy.order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_task_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'deploy': deploy, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('deploy/deploy_list.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_list_detail')
def deploy_list_form_add(request, *args, **kwargs):
    git_tools = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    id = kwargs['id']
    userinfo = models.userInfo.objects.all()
    deploy = models.deploy_app.objects.filter(id=id)
    proj_id = deploy.values('proj_id')[0]['proj_id']
    proj_name = deploy.values('proj_name')[0]['proj_name']
    proj = git_tools.projects.get(proj_id)
    branches = proj.branches.list()
    tags = proj.tags.list()
    # hostInfo = models.Server.objects.all()
    qs_deploy_type = models.DeployType.objects.all()
    msg = {'id': id, 'login_user': user_dict['user'], 'status': '操作成功',
           'deploy': deploy, 'userinfo': userinfo,
           'branches': branches, 'tags': tags, 'qs_deploy_type': qs_deploy_type,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('deploy/deploy_list_add.html', msg)


'''
@custom_login_required
@custom_permission_required('myapp.add_deploy_list_detail')
def deploy_list_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    user_dict = request.session.get('is_login', None)
    try:
        max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
    except:
        # 如果数据库为空，则从 ID 为 1 的数据开始提取
        max_id = 0
    # print(max_id, type(max_id))
    if request.method == 'POST':
        unit = request.POST.get('unit', None)
        proj_name = request.POST.get('proj_name', None)
        proj_id = request.POST.get('proj_id', None)
        tag = request.POST.get('tag', None)
        scriptType = request.POST.get('scriptType', None)
        # print(proj_name, type(proj_name), proj_id, type(proj_id), tag, type(tag), scriptType, type(scriptType))
        if scriptType == 'python':
            interpreter = 'python'
        if scriptType == 'shell':
            interpreter = 'sh'
        is_empty = all([proj_id, proj_name, ])
        if tag == 'NULL':
            status = 'tag为空，请重新选择tag！！！'
            msg = {'status': status, }
        elif not is_empty:
            status = '项目id或名称为空，请重新配置！！！'
            msg = {'status': status, }
        else:

            # result = tasks.ssh_remote.delay('192.168.38.129', 22, 'root', 'redhat',
            # 'python /root/gitlab/import/OneKeyDeploy.py' + ' ' + proj_id + ' ' + proj_name + ' ' + tag)
            ret = tasks.deploy_ssh_remote_exec_cmd.delay(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD,
                                                         SSH_CMD + ' ' + proj_id + ' ' + proj_name + ' '
                                                         + tag + ' ' + str(max_id + 1)
                                                         )

            # tasks.add_deploy_list_detail.delay(proj_name,tag,result)

            status = '提交成功！'
            msg = {'status': status, }
            # print (ret,type(ret))

        models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                                 tag=tag, task_id=ret, status="执行中")
        # 2023/08/17

        # tasks.create_deploy_list_detail.delay(unit,proj_name,proj_id,tag,ret,status)
        # print(msg)

    # return render_to_response('deploy/deploy_list.html', msg)
    return redirect('/cmdb/index/deploy/task/list/')
'''


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list_log(request, *args, **kwargs):
    id = kwargs['id']
    deploy = models.deploy_list_detail.objects.filter(id=id)
    proj_name = deploy.values('proj_name')[0]['proj_name']
    proj_id = deploy.values('proj_id')[0]['proj_id']
    task_id = deploy.values('task_id')[0]['task_id']
    tag = deploy.values('tag')[0]['tag']

    count = deploy.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)

    # ajax获取任务日志使用
    """
    result = AsyncResult(task_id)

    if result.ready():

        if result.successful():
            #result_value = result.get()
            result_value = result.result

        if result.failed():
            result_value = result.traceback

    else:
        result_value = ' '

    msg = {'deploy': deploy, 'login_user': userDict['user'], 'count': count,'result':result_value,
           'proj_name':proj_name,'end_time':result.date_done,'task_id':task_id,'tag':tag,'proj_id':proj_id,'id':id}
    """
    msg = {'deploy': deploy, 'login_user': user_dict['user'], 'count': count,
           'proj_name': proj_name, 'task_id': task_id, 'tag': tag, 'proj_id': proj_id, 'id': id,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(task_id, type(task_id), result, type(result),result.status,result.result,result.traceback,result.date_done,)
    # print(msg)
    return render_to_response('deploy/deploy_list_log.html', msg)


"""
@custom_login_required
def get_task_info(request,*args,**kwargs):
    task_id = request.POST.get('task_id',None)
    result = AsyncResult(task_id)
    #print(result.status)
    # ajax获取任务日志使用
    
    while result.result:
        models.deploy_list_detail.objects.filter(task_id=task_id).update(task_log=result.result,status=result.status)
        break
    
    #output = result.result

    task_status = models.deploy_list_detail.objects.filter(task_id=task_id).values('status')[0]['status']

    if result.status == 'SUCCESS' or result.status == 'FAILURE':
        task_status = '已完成'
        models.deploy_list_detail.objects.filter(task_id=task_id).update(status=task_status)

    task_log = models.deploy_list_detail.objects.filter(task_id=task_id).values('task_log')[0]['task_log']
    msg = {'task_log':task_log,'status':task_status}
    #return result.result #AttributeError: 'str' object has no attribute 'get'
    return HttpResponse(json.dumps(msg))
    """


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def get_task_info(request, *args, **kwargs):
    deploy_id = request.POST.get('id', None)
    task_status = models.deploy_list_detail.objects.filter(id=deploy_id).values('status')[0]['status']
    msg = {'status': task_status, 'id': deploy_id, }
    return HttpResponse(json.dumps(msg))


'''
@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list_cancel(request, *args, **kwargs):
    id = kwargs['id']
    deploy = models.deploy_list_detail.objects.filter(id=id)
    task_id = deploy.values('task_id')[0]['task_id']
    task_staus = deploy.values('status')[0]['status']
    proj_id = deploy.values('proj_id')[0]['proj_id']
    proj_name = deploy.values('proj_name')[0]['proj_name']
    tag = deploy.values('tag')[0]['tag']
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if task_staus == '执行中':
        # revoke未生效1
        # result = AsyncResult(task_id)
        # result.revoke(terminate=True,)
        # revoke未生效2
        # celery_control = Control(app=app)
        # res = celery_control.revoke(task_id=task_id,terminate=True)
        # print(res,type(res))
        msg = {'deploy': deploy, 'login_user': user_dict['user'], 'task_id': task_id, 'id': id}
        # print(task_id, type(task_id), result, type(result),result.status,result.result,result.traceback,result.date_done,)
        # print(msg)
        cancel_cmd = "ps -ef |grep " + SSH_SCRIPT_NAME + " |grep " + proj_id + " |grep " + proj_name + " |grep " + tag + " |grep " + id + " |grep -v grep |awk '{print $3}' |xargs kill -9"
        # print(cancel_cmd)
        # 取消异步执行
        # tasks.deploy_cancel_ssh_remote_exec_cmd.delay(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, cancel_cmd)
        tasks.deploy_cancel_ssh_remote_exec_cmd(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, cancel_cmd)
        models.deploy_list_detail.objects.filter(task_id=task_id).update(status='已取消', )
        return redirect('/cmdb/index/deploy/task/list/')
    elif task_staus == '已取消':
        msg = {'status': '任务已经取消过了，不要重复操作！'}
        return render_to_response('500.html', msg, status=500)
    else:
        msg = {'status': '任务已经结束，不能执行此操作！'}
        return render_to_response('500.html', msg, status=500)
'''


@custom_login_required
def deploy_sum(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    deploy_app = models.deploy_app.objects.all()
    labels = []
    data = []
    for item in deploy_app:
        labels.append(item.proj_name)
        deploy_list_detail = models.deploy_list_detail.objects.filter(proj_name=item.proj_name).count()
        data.append(deploy_list_detail)
    # print(labels, type(labels))
    # print(data, type(data))
    msg = {'labels': labels, 'login_user': user_dict['user'],
           'data': data, 'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return HttpResponse(json.dumps(msg))


@custom_login_required
def deploy_sum_yearly(request, *args, **kwargs):
    # 2024/01/09 当前年份数据统计
    today = datetime.datetime.today()
    year = today.year
    # year = 2023
    # month = today.month
    # print(today, year, month)

    data_monthly = []
    '''
    # update_time__month 查询不到数据
    for month in range(1, 13):
        deploy_monthly = models.deploy_list_detail.objects.filter(
            update_time__year=year, update_time__month=month
        ).count()
        data_monthly.append(deploy_monthly)
    '''

    for i in range(1, 13):
        if i == 12:
            start_date = datetime.date(year, i, 1)
            end_date = datetime.date(year + 1, 1, 1)
        else:
            start_date = datetime.date(year, i, 1)
            end_date = datetime.date(year, i + 1, 1)
        deploy_monthly = models.deploy_list_detail.objects.filter(update_time__range=(start_date, end_date)).count()
        # print(deploy_monthly)
        data_monthly.append(deploy_monthly)

    data_yearly_success = models.deploy_list_detail.objects.filter(update_time__year=year).filter(
        status='成功').count()
    data_yearly_fail = models.deploy_list_detail.objects.filter(update_time__year=year).filter(
        status='失败').count()
    data_yearly_withdraw = models.deploy_list_detail.objects.filter(update_time__year=year).filter(
        status='已取消').count()

    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)

    msg = {'login_user': user_dict['user'], 'data_monthly': data_monthly,
           'data_yearly_success': data_yearly_success, 'data_yearly_fail': data_yearly_fail,
           'data_yearly_withdraw': data_yearly_withdraw, 'wf_count_pending': wf_dict['wf_count_pending'],
           }
    # print(msg)
    return HttpResponse(json.dumps(msg))


@custom_login_required
@custom_permission_required('myapp.view_ansiblevars')
def ansible_vars(request, *args, **kwargs):
    qs = models.AnsibleVars.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'ansible_vars': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/ansible_vars.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_ansiblevars')
def ansible_vars_form_add(request, *args, **kwargs):
    qs = models.AnsibleVars.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'ansible_vars': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/ansible_vars_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_ansiblevars')
def ansible_vars_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        vars = request.POST.get('vars', None)
        is_exist = models.AnsibleVars.objects.filter(name=name)
        print(is_exist)
        if not is_exist:
            is_empty = all([name, ])
            if is_empty:
                models.AnsibleVars.objects.create(name=name, vars=vars, )
                msg = {'name': name,
                       'login_user': user_dict['user'], 'status': '添加Ansible变量成功', }
                return redirect('/cmdb/index/deploy/ansible-vars/list/')
            else:
                msg = {'name': name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'name': name,
                   'login_user': user_dict['user'], 'status': '该Ansible变量已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('deploy/ansible_vars_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_ansiblevars')
def ansible_vars_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AnsibleVars.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'ansible_vars': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('deploy/ansible_vars_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_ansiblevars')
def ansible_vars_update(request, *args, **kwargs):
    form_id = kwargs['id']
    name = request.POST.get('name')
    form_vars = request.POST.get('vars')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AnsibleVars.objects.filter(id=form_id).update(name=name, vars=form_vars, )
    return redirect('/cmdb/index/deploy/ansible-vars/list/')


@custom_login_required
@custom_permission_required('myapp.delete_ansiblevars')
def ansible_vars_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AnsibleVars.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除Ansible变量成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('deploy/ansible_vars.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_list_detail')
def deploy_list_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    user_dict = request.session.get('is_login', None)
    try:
        max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
    except IndexError:
        # 如果数据库为空，则返回0:
        max_id = 0
    # print(max_id, type(max_id))
    if request.method == 'POST':
        # 2024/6/5
        tomcat_job = TOMCAT_JOB_LIST
        unit = request.POST.get('unit', None)
        unit_id = get_object_or_404(models.wf_business, name=unit)
        qs_asset = models.Asset.objects.filter(business_unit_id=unit_id)
        # 通过value_list 获取ansible_vars外键中的字段
        host_list = list(qs_asset.values_list('ip', 'ansible_vars__vars'))
        print(host_list)
        proj_name = request.POST.get('proj_name', None)
        proj_id = request.POST.get('proj_id', None)
        tag = request.POST.get('tag', None)
        deploy_type_id = request.POST.get('deploy_type', None)
        print(deploy_type_id, type(deploy_type_id))   # str类型
        # print(proj_name, type(proj_name), proj_id, type(proj_id), tag, type(tag), scriptType, type(scriptType))
        if proj_name in tomcat_job:
            job_name = "build_java_prod"
        else:
            job_name = "build_java"
        log_dir = os.path.join(ANSIBLE_BASE_DIR, 'logs')  # 设置日志目录
        log_file_path = os.path.join(log_dir, f"ansible_deploy-{max_id + 1}.log")

        if deploy_type_id == '1':
            if tag == 'NULL':
                status = 'tag为空，请重新选择tag！！！'
                msg = {'status': status, }
                return render_to_response('500.html', msg, status=500)

            # 执行发布
            ret = tasks.deploy_main.delay(unit, host_list, GITLAB_URL, {"PRIVATE-TOKEN": GITLAB_TOKEN, },
                                          os.path.join(ANSIBLE_BASE_DIR, 'temp_download'),
                                          os.path.join(ANSIBLE_BASE_DIR, 'temp_unzip'),
                                          os.path.join(ANSIBLE_BASE_DIR, 'roles'),
                                          proj_name, proj_id, tag, job_name,
                                          os.path.join(ANSIBLE_BASE_DIR, 'inventory', f'{unit}.ini'),
                                          os.path.join(ANSIBLE_BASE_DIR, f'{proj_name}.yml'),
                                          str(max_id + 1), log_file_path, deploy_type_id
                                          )
            # 发布记录写入数据库
            models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                                     tag=tag, task_id=ret.id, status="执行中", type_id=deploy_type_id
                                                     )
        elif deploy_type_id == '2':
            tag = "---"
            # 执行发布
            ret = tasks.deploy_main.delay(unit, host_list, GITLAB_URL, {"PRIVATE-TOKEN": GITLAB_TOKEN, },
                                          os.path.join(ANSIBLE_BASE_DIR, 'temp_download'),
                                          os.path.join(ANSIBLE_BASE_DIR, 'temp_unzip'),
                                          os.path.join(ANSIBLE_BASE_DIR, 'roles'),
                                          proj_name, proj_id, tag, job_name,
                                          os.path.join(ANSIBLE_BASE_DIR, 'inventory', f'{unit}.ini'),
                                          os.path.join(ANSIBLE_BASE_DIR, f'{proj_name}.yml'),
                                          str(max_id + 1), log_file_path, deploy_type_id
                                          )
            # 发布记录写入数据库
            models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                                     tag=tag, task_id=ret.id, status="执行中", type_id=deploy_type_id
                                                     )

        return redirect('/cmdb/index/deploy/task/list/')
    return render_to_response('500.html', status=405)


# celery revoke未成功，暂时不可用
@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list_cancel(request, *args, **kwargs):
    deploy_id = kwargs['id']
    deploy = models.deploy_list_detail.objects.filter(id=deploy_id).first()
    if not deploy:
        msg = {'status': '任务不存在'}
        return render_to_response('500.html', msg, status=500)

    task_id = deploy.task_id
    task_status = deploy.status

    if task_status == '执行中':
        tasks.deploy_cancel.delay(deploy_id, task_id)
        # 更新数据库中任务状态
        deploy.status = '已取消'
        deploy.save()

        # 记录日志
        print(f"任务 {task_id} 成功撤销")
        return redirect('/cmdb/index/deploy/task/list/')
    elif task_status == '已取消':
        msg = {'status': '任务已经取消过了，不要重复操作！'}
        return render_to_response('500.html', msg, status=500)
    else:
        msg = {'status': '任务已经结束，不能执行此操作！'}
        return render_to_response('500.html', msg, status=500)
