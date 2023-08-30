#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import time

from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from apps.myapp import models
from django.shortcuts import redirect
from apps.myapp import tasks, common, page_helper
from apps.myapp import token_helper
from django.utils import timezone
import os, json
from django.http import JsonResponse
from django.core import serializers
from celery import chord, group, chain
from django.db.models import Q
from apps.myapp.gitlab_helper import GitTools
import gitlab
import paramiko, subprocess
from apps.myapp import loop
from django.core.cache import cache
from myweb.settings import GITLAB_URL, GITLAB_TOKEN
from apps.myapp.paramiko_ssh_helper import ssh_remote
from celery.result import AsyncResult
from myweb.settings import SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, SSH_CMD, SSH_WORKDIR


@custom_login_required
@custom_permission_required('myapp.view_deploy_script_type')
def deploy_script_type(request, *args, **kwargs):
    scripttype = models.deploy_script_type.objects.all()
    count = scripttype.count()
    userDict = request.session.get('is_login', None)
    msg = {'scripttype': scripttype, 'login_user': userDict['user'], 'count': count}
    return render_to_response('deploy/script_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_script_type')
def deploy_script_type_form_add(request, *args, **kwargs):
    scripttype = models.deploy_script_type.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'scripttype': scripttype, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('deploy/script_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_script_type')
def deploy_script_type_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    scripttype = models.deploy_script_type.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'scripttype': scripttype, }
    print(msg)
    return render_to_response('deploy/script_type_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_script_type')
def deploy_script_type_add(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        scripttype = request.POST.get('scripttype', None)
        is_exist = models.deploy_script_type.objects.filter(name=scripttype)
        # print(is_exist)
        if not (is_exist):
            is_empty = all([scripttype, ])
            if is_empty:
                models.deploy_script_type.objects.create(name=scripttype, )
                msg = {'scripttype': scripttype, 'login_user': userDict['user'], 'status': '添加脚本类型成功', }
                return redirect('/cmdb/index/deploy/scripttype/list/')
            else:
                msg = {'scripttype': scripttype, 'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            msg = {'scripttype': scripttype, 'login_user': userDict['user'], 'status': '该脚本类型已存在！', }
    return render_to_response('deploy/script_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_script_type')
def deploy_script_type_update(request, *args, **kwargs):
    id = kwargs['id']
    scripttype = request.POST.get('scripttype')
    userDict = request.session.get('is_login', None)
    models.deploy_script_type.objects.filter(id=id).update(name=scripttype, )
    return redirect('/cmdb/index/deploy/scripttype/list/')


@custom_login_required
@custom_permission_required('myapp.delete_deploy_script_type')
def deploy_script_type_del(request, *args, **kwargs):
    id = request.POST.get('id')
    models.deploy_script_type.objects.filter(id=id).delete()
    # print('delete', id)
    msg = {'code': 1, 'result': '删除脚本类型id:' + id, }
    return render_to_response('deploy/script_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_app')
def deploy_app(request, *args, **kwargs):
    count = models.deploy_app.objects.all().count()
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    userDict = request.session.get('is_login', None)
    deploy = models.deploy_app.objects.all()[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_app_list(request, page, pageinfo.pageCount)
    msg = {'deploy': deploy, 'login_user': userDict['user'], 'count': count,
           'pageCount': pageinfo.pageCount, 'page': page_string, }
    return render_to_response('deploy/deploy_app.html', msg)


@custom_login_required
def deploy_app_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/deploy/app/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/deploy/app/list/')


@custom_login_required
def deploy_app_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    deploy = models.deploy_app.objects.filter(proj_name__icontains=keyword) | models.deploy_app.objects.filter(
        proj_id__icontains=keyword)
    count = deploy.count()
    userDict = request.session.get('is_login', None)
    page = common.try_int(kwargs['page'], 1)
    print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    deploy = deploy[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_app_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'deploy': deploy, 'login_user': userDict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string, }
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
    userDict = request.session.get('is_login', None)
    msg = {'business': business, 'userinfo': userinfo, 'deploy': deploy,
           'login_user': userDict['user'], 'status': '', 'approval': approval, }
    print(msg)
    return render_to_response('deploy/deploy_app_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_app')
def deploy_app_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    business = models.wf_business.objects.all()
    if request.method == 'POST':
        unit_id = request.POST.get('unit', None)
        unit = models.wf_business.objects.filter(id=unit_id).values('name')[0]['name']
        proj_name = request.POST.get('proj_name', None)
        proj_id = request.POST.get('proj_id', None)
        is_exist = models.deploy_app.objects.filter(proj_name=proj_name)
        print(is_exist)
        if not (is_exist):
            is_empty = all([proj_id, proj_name, unit])
            if is_empty:
                queryset = models.deploy_app.objects.create(unit_id=unit_id, proj_id=proj_id, proj_name=proj_name, )
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': userDict['user'], 'status': '添加应用成功', }
                return redirect('/cmdb/index/deploy/app/list/')
            else:
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'business': business,
                   'login_user': userDict['user'], 'status': '该应用已存在！', }
    return render_to_response('deploy/deploy_app_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_app')
def deploy_app_form_update(request, *args, **kwargs):
    id = kwargs['id']
    deploy = models.deploy_app.objects.filter(id=id)
    business = models.wf_business.objects.all().exclude(unit__id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': u'操作成功', 'deploy': deploy, 'business': business}
    print(msg)
    return render_to_response('deploy/deploy_app_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_deploy_app')
def deploy_app_update(request, *args, **kwargs):
    id = kwargs['id']
    unit_id = request.POST.get('unit', None)
    unit = models.wf_business.objects.filter(id=unit_id).values('name')
    print(unit)
    proj_name = request.POST.get('proj_name', None)
    proj_id = request.POST.get('proj_id', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.deploy_app.objects.filter(id=id).update(unit_id=unit_id, proj_id=proj_id, proj_name=proj_name,
                                                   update_time=update_time, )
    return redirect('/cmdb/index/deploy/app/list/')


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def deploy_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            wfbusiness_id = request.POST.get('wfbusiness', None)
            print(wfbusiness_id)
            wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id)
            director_id = wfbusiness.values('director_id')[0]['director_id']
            director = models.userInfo.objects.filter(id=director_id).values('username')[0]['username']
            print(wfbusiness, director_id, director, )
            userDict = request.session.get('is_login', None)
            # data = serializers.serialize('json',wfbusiness) #序列化
            # data = json.dumps(wfbusiness)
            data = {'director_id': director_id, 'director': director, }
            print(data)
            # return HttpResponse(json.dumps(data))
        except:
            data = {'director_id': '0', 'director': '------------- 请选择 -------------', }
        finally:
            return HttpResponse(json.dumps(data))


@custom_login_required
@custom_permission_required('myapp.delete_deploy_app')
def deploy_app_del(request, *args, **kwargs):
    id = request.POST.get('id')
    models.deploy_app.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除app id:' + id, }
    return render_to_response('deploy/deploy_app.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_deploy_list_detail')
def deploy_list(request, *args, **kwargs):
    count = models.deploy_list_detail.objects.all().count()
    userDict = request.session.get('is_login', None)
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    # 发布列表降序排列
    deploy = models.deploy_list_detail.objects.all().order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_task_list(request, page, pageinfo.pageCount)

    msg = {'deploy': deploy, 'login_user': userDict['user'], 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, }
    return render_to_response('deploy/deploy_list.html', msg)


@custom_login_required
def deploy_list_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/deploy/task/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/deploy/task/list/')


@custom_login_required
def deploy_list_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    deploy = models.deploy_list_detail.objects.filter(
        proj_name__icontains=keyword) | models.deploy_list_detail.objects.filter(status__icontains=keyword)
    count = deploy.count()
    userDict = request.session.get('is_login', None)
    page = common.try_int(kwargs['page'], 1)
    print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    deploy = deploy.order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_deploy_task_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'deploy': deploy, 'login_user': userDict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string, }
    # return render_to_response('user_search.html',msg)
    return render_to_response('deploy/deploy_list.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_list_detail')
def deploy_list_form_add(request, *args, **kwargs):
    git_tools = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN)
    userDict = request.session.get('is_login', None)
    id = kwargs['id']
    userinfo = models.userInfo.objects.all()
    deploy = models.deploy_app.objects.filter(id=id)
    proj_id = deploy.values('proj_id')[0]['proj_id']
    proj_name = deploy.values('proj_name')[0]['proj_name']
    proj = git_tools.projects.get(proj_id)
    branches = proj.branches.list()
    tags = proj.tags.list()
    userDict = request.session.get('is_login', None)
    hostInfo = models.Server.objects.all()
    scriptType = models.deploy_script_type.objects.all()
    # print(scriptType,type(scriptType))
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功',
           'deploy': deploy, 'userinfo': userinfo,
           'branches': branches, 'tags': tags, 'hostInfo': hostInfo,
           'scriptType': scriptType}
    # print(msg)
    return render_to_response('deploy/deploy_list_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_deploy_list_detail')
def deploy_list_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    try:
        max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
    except:
        # 如果数据库为空，则从 ID 为 1 的数据开始提取
        max_id = 0
    print(max_id, type(max_id))
    if request.method == 'POST':
        unit = request.POST.get('unit', None)
        proj_name = request.POST.get('proj_name', None)
        proj_id = request.POST.get('proj_id', None)
        tag = request.POST.get('tag', None)
        scriptType = request.POST.get('scriptType', None)
        print(proj_name, type(proj_name), proj_id, type(proj_id), tag, type(tag), scriptType, type(scriptType))
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
            # 'python /root/gitlab/download/OneKeyDeploy.py' + ' ' + proj_id + ' ' + proj_name + ' ' + tag)
            ret = tasks.ssh_remote_exec_cmd.delay(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD,
                                                  SSH_CMD + ' ' + proj_id + ' ' + proj_name + ' ' + tag + ' ' + str(
                                                      max_id + 1))
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
    userDict = request.session.get('is_login', None)

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
    msg = {'deploy': deploy, 'login_user': userDict['user'], 'count': count,
           'proj_name': proj_name, 'task_id': task_id, 'tag': tag, 'proj_id': proj_id, 'id': id}
    # print(task_id, type(task_id), result, type(result),result.status,result.result,result.traceback,result.date_done,)
    print(msg)
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
    id = request.POST.get('id', None)
    # print(id,type(id),task_id,)
    task_status = models.deploy_list_detail.objects.filter(id=id).values('status')[0]['status']
    msg = {'status': task_status, 'id': id, }
    return HttpResponse(json.dumps(msg))
