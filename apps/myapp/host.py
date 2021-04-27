#!/usr/bin/env python
#coding:utf-8

from apps.myapp.login_required import outer
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
from apps.myapp.mygitlab import GitTools
import gitlab




@outer
def hostForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    wfbusiness = models.wf_business.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'userinfo':userinfo,
           'usergroup':usergroup,'login_user': userDict['user'],'status':'', }
    print(msg)
    return render_to_response('workflow/wfbusiness_add.html',msg)

@outer
def hostForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    userinfo = models.userInfo.objects.all()
    usergroup = models.userGroup.objects.all()
    wfbusiness = models.wf_business.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功',
           'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,}
    print(msg)
    return render_to_response('workflow/wfbusiness_update.html',msg)


@outer
def hostForm_deploy(request,*args,**kwargs):
    git_url = 'http://10.180.11.8'
    git_token = 'F7nAGXozy4dsfJvxiLu_'
    git_tools = gitlab.Gitlab(git_url,git_token)
    #userid = request.GET.get('userid',None)
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
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功',
           'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,
           'branches':branches,'tags':tags}
    print(msg)
    return render_to_response('workflow/wfbusiness_deploy.html',msg)

@outer
def hostAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        wfbusiness = request.POST.get('wfbusiness',None)
        repo = request.POST.get('repo', None)
        director_id = request.POST.get('director',None)
        group_id = request.POST.get('group',None)
        is_exist = models.wf_business.objects.filter(name=wfbusiness)
        print(is_exist)
        if not (is_exist):
            is_empty = all([wfbusiness,repo])
            if is_empty:
                models.wf_business.objects.create(name=wfbusiness,repo=repo,director_id=director_id,group_id=group_id)
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': userDict['user'],'status':'添加业务单元成功', }
                return redirect('/cmdb/index/wf/wfbusiness/')
            else:
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该业务单元已存在！', }
    return render_to_response('workflow/wfbusiness_add.html',msg)

@outer
def host(request,*args,**kwargs):
    wfbusiness=models.wf_business.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'login_user': userDict['user'],}
    return render_to_response('workflow/wfbusiness.html',msg)



def hostDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_business.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除工单类型id:'+id,}
    return render_to_response('workflow/wfbusiness.html',msg)

def hostUpdate(request,*args,**kwargs):
    id = kwargs['id']
    wfbusiness_id = request.POST.get('wfbusiness')
    wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id).values('name')[0]['name']
    director_id = request.POST.get('director')
    group_id = request.POST.get('group')
    repo = request.POST.get('repo')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.wf_business.objects.filter(id=id).update(name=wfbusiness,
        update_time=update_time,director_id=director_id,group_id=group_id,repo=repo)
    return redirect('/cmdb/index/wf/wfbusiness/')


