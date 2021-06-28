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
from django.contrib.auth.models import Group

@custom_login_required
@custom_permission_required('myapp.view_wf_type')
def wftype(request,*args,**kwargs):
    wftype=models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wftype': wftype, 'login_user': userDict['user'],}
    return render_to_response('workflow/wftype.html',msg)

@custom_login_required
@custom_permission_required('myapp.add_wf_type')
def wftypeForm_add(request,*args,**kwargs):
    #userinfo = models.userInfo.objects.all()
    wftype = models.wf_type.objects.all()
    #usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wftype': wftype, 'login_user': userDict['user'],'status':'', }
    return render_to_response('workflow/wftype_add.html',msg)

@custom_login_required
@custom_permission_required('myapp.add_wf_type')
def wftypeAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    #usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    #usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        wftype = request.POST.get('wftype',None)
        is_exist = models.wf_type.objects.filter(name=wftype)
        print(is_exist)
        if not (is_exist):
            is_empty = all([wftype,])
            if is_empty:
                models.wf_type.objects.create(name=wftype,)
                msg = {'userinfo': userinfo, 'wftype': wftype,
                       'login_user': userDict['user'],'status':'添加工单类型成功', }
                return redirect('/cmdb/index/wf/wftype/')
            else:
                msg = {'userinfo': userinfo, 'wftype': wftype,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'wftype': wftype,
                   'login_user': userDict['user'],'status':'该工单类型已存在！', }
    return render_to_response('workflow/wftype_add.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_type')
def wftypeForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    wftype = models.wf_type.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功','wftype':wftype,}
    print(msg)
    return render_to_response('workflow/wftype_update.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_type')
def wftypeUpdate(request,*args,**kwargs):
    id = kwargs['id']
    wftype = request.POST.get('wftype')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.wf_type.objects.filter(id=id).update(name=wftype,update_time=update_time)
    return redirect('/cmdb/index/wf/wftype/')

@custom_login_required
@custom_permission_required('myapp.delete_wf_type')
def wftypeDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_type.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除工单类型id:'+id,}
    return render_to_response('workflow/wftype.html',msg)

@custom_login_required
@custom_permission_required('myapp.view_wf_business')
def wfbusiness(request,*args,**kwargs):
    wfbusiness=models.wf_business.objects.all()
    count=wfbusiness.count()
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'login_user': userDict['user'],'count':count,}
    return render_to_response('workflow/wfbusiness.html',msg)

@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def wfbusinessForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    wfbusiness = models.wf_business.objects.all()
    #usergroup = models.userGroup.objects.all()
    approval = userinfo.exclude(workflow_order=0)
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'userinfo':userinfo,
           'login_user': userDict['user'],'status':'','approval':approval, }
    print(msg)
    return render_to_response('workflow/wfbusiness_add.html',msg)

@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def wfbusinessAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        wfbusiness = request.POST.get('wfbusiness',None)
        repo = request.POST.get('repo', None)
        admin_id = request.POST.get('admin',None)
        approval = request.POST.getlist('approval',None)
        is_exist = models.wf_business.objects.filter(name=wfbusiness)
        print(is_exist)
        if not (is_exist):
            is_empty = all([wfbusiness,repo])
            if is_empty:
                queryset=models.wf_business.objects.create(name=wfbusiness,repo=repo,admin_id=admin_id,)
                queryset.approval.set(approval)
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': userDict['user'],'status':'添加业务单元成功', }
                return redirect('/cmdb/index/wf/wfbusiness/')
            else:
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                   'login_user': userDict['user'],'status':'该业务单元已存在！', }
    return render_to_response('workflow/wfbusiness_add.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusinessForm_update(request,*args,**kwargs):
    id = kwargs['id']
    wfbusiness = models.wf_business.objects.filter(id=id)
    admin = models.userInfo.objects.all().exclude(admin__id=id)
    approval = models.userInfo.objects.all().exclude(workflow_order=0).exclude(approval__id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':u'操作成功','wfbusiness':wfbusiness,
           'admin':admin,'approval':approval,}
    print(msg)
    return render_to_response('workflow/wfbusiness_update.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusinessUpdate(request,*args,**kwargs):
    id = kwargs['id']
    wfbusiness_id = request.POST.get('wfbusiness')
    wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id).values('name')[0]['name']
    admin_id = request.POST.get('admin')
    approval = request.POST.getlist('approval')
    repo = request.POST.get('repo')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.wf_business.objects.filter(id=id).update(name=wfbusiness,
        update_time=update_time,admin_id=admin_id,repo=repo)
    models.wf_business.objects.get(id=id).approval.set(approval)
    return redirect('/cmdb/index/wf/wfbusiness/')

@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusiness_ajax(request,*args,**kwargs):
    if request.method == 'POST':
        try:
            wfbusiness_id = request.POST.get('wfbusiness',None)
            print(wfbusiness_id)
            wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id)
            director_id = wfbusiness.values('director_id')[0]['director_id']
            director = models.userInfo.objects.filter(id=director_id).values('username')[0]['username']
            print(wfbusiness,director_id,director,)
            userDict = request.session.get('is_login', None)
            #data = serializers.serialize('json',wfbusiness) #序列化
            #data = json.dumps(wfbusiness)
            data = {'director_id':director_id,'director':director,}
            print(data)
            #return HttpResponse(json.dumps(data))
        except:
            data = {'director_id':'0','director':'------------- 请选择 -------------',}
        finally:
            return HttpResponse(json.dumps(data))

@custom_login_required
@custom_permission_required('myapp.delete_wf_business')
def wfbusinessDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_business.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除工单类型id:'+id,}
    return render_to_response('workflow/wfbusiness.html',msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def wf(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'login_user': userDict['user'], 'wf_info': wf_info,'userinfo':userinfo,}
    return render_to_response('workflow/workflow.html',msg)

@custom_login_required
@custom_permission_required('myapp.add_wf_info')
def wrokflow_form_add(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    #user_group = models.userGroup.objects.all()
    user_info = models.userInfo.objects.all()
    wf_business = models.wf_business.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method=='GET':
        msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status':'', 'wf_type':wf_type,
               'user_info':user_info,'wf_business':wf_business}
        print(msg,)
        return render_to_response('workflow/workflow_add.html',msg)
    if request.method=='POST':

        '''
        dest=open(os.path.join("F:\\upload",files),'wb+')
        for chunk in files.chunks():
            dest.write(chunk)
        dest.close()
        '''

        '''
        path = default_storage.save('temp/dj', ContentFile(files.read()))
        temp_file = os.path.join(settings.MEDIA_ROOT, path)
        status='上传完成'
        msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': status,
               'wf_type': wf_type, 'user_group': user_group, 'fileName':fileName}
        print(msg,)
        print(path,)
        print(temp_file,)
        return render_to_response('workflow/workflow_add.html', msg)
        '''
        try:
            mf=request.FILES.get('mf')
            print(mf,type(mf),)
            print(mf.read,)
            fileName=request.POST.get('fileName')
            print(fileName,type(fileName),)
            uploadDir='C:/upload/'
            if not os.path.exists(uploadDir):
                os.mkdir(uploadDir)
            fileName=uploadDir+fileName
            with open(fileName,'wb+',) as f:
                for chunk in mf:
                    f.write(chunk)
            status = '上传完成'
            msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': status,
                'wf_type': wf_type, 'user_group': user_group, }
            print(msg, )
            return render_to_response('workflow/workflow_add.html', msg)
        except Exception as e:
            print('error:',e)

@custom_login_required
@custom_permission_required('myapp.add_wf_info')
def workflow_add(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    userinfo = models.userInfo.objects.all()

    if request.method == 'POST':
            sn = token_helper.get_random_uuid()
            title = request.POST.get('title')
            sponsor = request.POST.get('sponsor', None)
            memo = request.POST.get('memo', None)
            type_id = request.POST.get('type', None)
            try:
                type_select = models.wf_type.objects.get(id=type_id, )
            except:
                type_select = None
            '''
                    #get:instance,filter:QuerySet,Error:
                    Cannot assign "<QuerySet [<wf_type: wf_type object (1)>]>": "wf_info.types" must be a "wf_type" instance

                    action_id = request.POST.get('action',None)
                    action_select = models.wf_action.objects.get(id=action_id,)
                    '''
            content = request.POST.get('content', None)
            wfbusiness_id = request.POST.get('wf_business',None)
            try:
                wfbusiness_select = models.wf_business.objects.get(id=wfbusiness_id)
            except:
                wfbusiness_select = None
            is_empty = all([title,content,type_select,wfbusiness_select,])
            if is_empty:
                models.wf_info.objects.create(sn=sn, title=title, sponsor=sponsor, type=type_select,
                 content=content,  memo=memo,business=wfbusiness_select, )
                return redirect('/cmdb/index/wf/requests/list/')
            else:
                status = '带有*的选项不能为空！'
                msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'error': status,
                       'wf_type': wf_type, 'userinfo': userinfo, }
                return render_to_response('workflow/500.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_form_update(request,*args,**kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        obj = models.wf_info.objects.filter(sn=sn)
        status = obj.values('status')[0]['status']
        if status != "未提交":
            msg = {'error': '流程进行中，不能修改！'}
            return render_to_response('workflow/500.html', msg)
        else:
            title = obj.values('title')
            sponsor = obj.values('sponsor')
            business = models.wf_business.objects.filter(wf_info__sn=sn)
            type = models.wf_type.objects.filter(wf_info__sn=sn)
            content = obj.values('content')
            memo = obj.values('memo')
            userDict = request.session.get('is_login', None)
            msg = {'id':id,'sn':sn,'title':title,'sponsor':sponsor,'type':type,'login_user':userDict['user'],
                   'status':'操作成功',
                   'content':content,'memo':memo,'business':business}
            print(msg)
            return render_to_response('workflow/workflow_update.html',msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_update(request,*args,**kwargs):
    try:
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        sponsor = request.POST.get('sponsor')
        type = request.POST.get('type', None)
        type_select = models.wf_type.objects.get(name=type)
        title = request.POST.get('title')
        content = request.POST.get('content')
        memo = request.POST.get('memo')
        update_time = timezone.now()
        print(id,sponsor,type,content,memo,)
        #userDict = request.session.get('is_login', None)
        models.wf_info.objects.filter(sn=sn).update(title=title,sponsor=sponsor,type=type_select,
              content=content,memo=memo,update_time=update_time,)
        return render_to_response('workflow/workflow_update.html')
    except Exception as e:
        print(e,)
    finally:
        return redirect('/cmdb/index/wf/requests/list/')

@custom_login_required
@custom_permission_required('myapp.view_wf_info')
def workflow_detail(request,*args,**kwargs):
    sn = request.GET.get('sn',None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_info_process_start = models.wf_info_process_history.objects.filter(sn=sn).filter(status='已提交')
    wf_info_process = models.wf_info_process_history.objects.filter(sn=sn).exclude(status='已提交').exclude(status='已完成').order_by('flow_id')
    wf_info_process_end = models.wf_info_process_history.objects.filter(sn=sn).filter(status='已完成')
    userDict = request.session.get('is_login', None)
    msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status': '',
           'wf_info_process_start':wf_info_process_start,'wf_info_process':wf_info_process,'wf_info_process_end':wf_info_process_end}
    return render_to_response('workflow/workflow_detail.html',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_approve(request,*args,**kwargs):
    sn = request.GET.get('sn',None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    userDict = request.session.get('is_login', None)
    msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status': '',}
    return render_to_response('workflow/workflow_approve.html',msg)

@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_tasks(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    wf_info = models.wf_info.objects.filter(next_assignee=userDict['user']).filter(flow_id__gte=0).filter(~Q(status='已完成'))
    count_pending = wf_info.count()
    wf_info_process = models.wf_info_process_history.objects.filter(assignee=userDict['user']).filter(flow_id__gt=0)
    count_processing = wf_info_process.count()
    wf_type = models.wf_type.objects.all()
    msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': '',
           'wf_type': wf_type,'wf_info_process':wf_info_process,'count_pending':count_pending,'count_processing':count_processing,}
    print(msg,)
    return render_to_response('workflow/workflow_tasks.html',msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_requests(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    wf_info = models.wf_info.objects.filter(sponsor=userDict['user'])
    wf_type = models.wf_type.objects.all()
    msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': '',
           'wf_type': wf_type, }
    print(msg, )
    return render_to_response('workflow/workflow_requests.html', msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_commit(request,*args,**kwargs):
    if request.method=='GET':
        sn = kwargs['sn']
        userDict = request.session.get('is_login', None)
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        if status != "未提交":
            msg = {'error':'流程进行中，不能重复提交！'}
            return render_to_response('workflow/500.html',msg)
        else:
            #c1 = tasks.workflow_commit.apply_async((sn,), link=tasks.workflow_send_email.s(username, email))
            #print(list(c1.collect()),c1.children,c1.get(),)
            tasks.workflow_commit(sn)
            msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': '', }
            return redirect('/cmdb/index/wf/requests/list/',msg)

@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_withdraw(request,*args,**kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        flow_id = wf_info.values('flow_id')[0]['flow_id']
        if flow_id > 0:
            msg = {'error':'流程进行中，不能撤回！'}
            return render_to_response('workflow/500.html',msg)
        else:
            tasks.workflow_withdraw(sn)
            userDict = request.session.get('is_login', None)
            msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status': '', }
            return redirect('/cmdb/index/wf/requests/list/', msg)

@custom_login_required
def workflow_upload(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    #user_group = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        files = request.FILES.get('mf', None)
        print(files, )
        if not files:
            status = '没有文件上传'
            msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': status,
                   'wf_type': wf_type, }
            print(msg, )
            return render_to_response('workflow/workflow_add.html', msg)
        '''
        dest=open(os.path.join("F:\\upload",files),'wb+')
        for chunk in files.chunks():
            dest.write(chunk)
        dest.close()
        '''
        path = default_storage.save('temp/dj', ContentFile(files.read()))
        # temp_file = os.path.join(settings.MEDIA_ROOT, path)
        status = '上传完成'
        msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': status,
               'wf_type': wf_type, 'user_group': user_group, }
        print(msg, )
        return render_to_response('workflow/workflow_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_process(request,*args,**kwargs):
    if request.method=='POST':
        suggest = request.POST.get('suggest',None)
        suggest_agree=request.POST.get('suggest_agree',None)
        suggest_reject = request.POST.get('suggest_reject', None)
        sn = request.POST.get('sn', None)
        wf_info = models.wf_info.objects.filter(sn=sn)
        userDict = request.session.get('is_login', None)
        tasks.workflow_process(sn,suggest,suggest_agree,suggest_reject)
        msg = {'wf_info': wf_info, 'login_user': userDict['user'],
               'status': '',  }
        return redirect('/cmdb/index/wf/tasks/list/')

