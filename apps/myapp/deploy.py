#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from apps.myapp.auth_helper import custom_login_required,custom_permission_required
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from apps.myapp import models
from django.shortcuts import redirect
from apps.myapp import tasks
from apps.myapp import token_helper
from django.utils import timezone
import os,json
from django.http import JsonResponse
from django.core import serializers
from celery import chord,group,chain
from django.db.models import Q
from apps.myapp.gitlab_helper import GitTools
import gitlab
import paramiko,subprocess
from apps.myapp import loop
from django.core.cache import cache
from myweb.settings import GITLAB_URL,GITLAB_TOKEN




@custom_login_required
def scripttypeForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    scripttype = models.scriptType.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'scripttype': scripttype, 'login_user': userDict['user'],'status':'', }
    return render_to_response('workflow/scripttype_add.html',msg)



@custom_login_required
def scripttypeForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    scripttype = models.scriptType.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功','scripttype':scripttype,}
    print(msg)
    return render_to_response('workflow/scripttype_update.html',msg)


@custom_login_required
def scripttypeAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        scripttype = request.POST.get('scripttype',None)
        is_exist = models.scriptType.objects.filter(type=scripttype)
        print(is_exist)
        if not (is_exist):
            is_empty = all([scripttype,])
            if is_empty:
                models.scriptType.objects.create(type=scripttype,)
                msg = {'userinfo': userinfo, 'scripttype': scripttype,
                       'login_user': userDict['user'],'status':'添加脚本类型成功', }
                return redirect('/cmdb/index/script/scripttype/')
            else:
                msg = {'userinfo': userinfo, 'scripttype': scripttype,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'scripttype': scripttype, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该工单类型已存在！', }
    return render_to_response('workflow/scripttype_add.html',msg)



@custom_login_required
def scripttype(request,*args,**kwargs):
    scripttype=models.scriptType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'scripttype': scripttype, 'login_user': userDict['user'],}
    return render_to_response('workflow/scripttype.html',msg)



def scripttypeDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.scriptType.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除脚本类型id:'+id,}
    return render_to_response('workflow/scripttype.html',msg)


def scripttypeUpdate(request,*args,**kwargs):
    id = kwargs['id']
    scripttype = request.POST.get('scripttype')
    #update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.scriptType.objects.filter(id=id).update(type=scripttype,)
    return redirect('/cmdb/index/script/scripttype/')









@custom_login_required
def wfbusinessForm_deploy(request,*args,**kwargs):
    git_tools = gitlab.Gitlab(GITLAB_URL,GITLAB_TOKEN)
    #userid = request.GET.get('userid',None)
    userDict = request.session.get('is_login', None)
    id = kwargs['id']
    userinfo = models.userInfo.objects.all()
    usergroup = models.userGroup.objects.all()
    wfbusiness = models.wf_business.objects.filter(id=id)
    name = wfbusiness.values('name')[0]['name']
    proj_id = wfbusiness.values('proj_id')[0]['proj_id']
    proj = git_tools.projects.get(proj_id)
    branches = proj.branches.list()
    tags = proj.tags.list()
    userDict = request.session.get('is_login', None)
    hostInfo = models.Server.objects.all()
    scriptType = models.scriptType.objects.all()
    print(scriptType,type(scriptType))
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功',
           'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,
           'branches':branches,'tags':tags,'hostInfo':hostInfo,
           'scriptType':scriptType}
    print(msg)
    return render_to_response('workflow/wfbusiness_deploy.html',msg)


@custom_login_required
def wfbusiness_deploy(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    userDict = request.session.get('is_login', None)
    id = kwargs['id']
    userinfo = models.userInfo.objects.all()
    usergroup = models.userGroup.objects.all()
    wfbusiness = models.wf_business.objects.filter(id=id)
    host = request.POST.get('host')
    port = 22
    username = 'root'
    password = 'Eo3C%k5j'
    script_type = request.POST.get('script_type')
    command = request.POST.get('command')
    name = request.POST.get('name',None)
    proj_id = wfbusiness.values('proj_id')[0]['proj_id']
    repo = request.POST.get('repo',None)
    branch = request.POST.get('branch',None)
    tag = request.POST.get('tag','default')
    opertator = models.userInfo.objects.get(username=userDict['user'])
    update_time = timezone.now()
    hostInfo = models.hostInfo.objects.all()
    scriptType = models.scriptType.objects.all()
    # print(scriptType,type(scriptType))

    job = tasks.deploy.s(host, port, username, password, command,name).delay()
    state = job.state
    logs = cache.get(name)
    print(job,job.status,job.result,job.id)
    t= loop.LoopTimer(10,loop.wfbusiness_deploy_query,[job,name,proj_id,repo,branch,tag,opertator,update_time,])
    result = t.start()
    #print(result,)
    models.wf_business_deploy_history.objects.create(name=name, proj_id=proj_id, repo=repo,
                                                     branch=branch, tag=tag, opertator=opertator,
                                                     update_time=update_time, state=state,logs=logs,)
    msg = {'id':id, 'login_user':userDict['user'],'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,
           'hostInfo':hostInfo,'scriptType':scriptType,'status':'','login_user': userDict['user'],}
    #print(msg)
    return redirect('/cmdb/index/wf/wfbusiness/deploy/list/',msg)

@custom_login_required
def wfbusiness_deploy_list(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    wfbusiness = models.wf_business_deploy_history.objects.all()
    msg = {'wfbusiness':wfbusiness,'login_user': userDict['user'],}
    return render_to_response('workflow/wfbusiness_deploy_list.html',msg)

@custom_login_required
def wfbusiness_deploy_log(request,*args,**kwargs):
    id = kwargs['id']
    userDict = request.session.get('is_login', None)
    wfbusiness = models.wf_business_deploy_history.objects.filter(id=id)
    msg = {'wfbusiness':wfbusiness,'login_user': userDict['user'],}
    return render_to_response('workflow/wfbusiness_deploy_log.html',msg)

@custom_login_required
def wfbusiness_deploy_del(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_business_deploy_history.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除发布id:'+id,}
    return render_to_response('workflow/wfbusiness_deploy_list.html',msg)






