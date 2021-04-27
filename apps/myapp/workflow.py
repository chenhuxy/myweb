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
import paramiko,subprocess
from apps.myapp import loop



@outer
def wftypeForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    wftype = models.wf_type.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wftype': wftype, 'login_user': userDict['user'],'status':'', }
    return render_to_response('workflow/wftype_add.html',msg)


@outer
def wftypeForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    wftype = models.wf_type.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功','wftype':wftype,}
    print(msg)
    return render_to_response('workflow/wftype_update.html',msg)

@outer
def wftypeAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
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
            msg = {'userinfo': userinfo, 'wftype': wftype, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该工单类型已存在！', }
    return render_to_response('workflow/wftype_add.html',msg)

@outer
def wftype(request,*args,**kwargs):
    wftype=models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wftype': wftype, 'login_user': userDict['user'],}
    return render_to_response('workflow/wftype.html',msg)

def wftypeDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_type.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除工单类型id:'+id,}
    return render_to_response('workflow/wftype.html',msg)

def wftypeUpdate(request,*args,**kwargs):
    id = kwargs['id']
    wftype = request.POST.get('wftype')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.wf_type.objects.filter(id=id).update(name=wftype,update_time=update_time)
    return redirect('/cmdb/index/wf/wftype/')



@outer
def wfbusinessForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    wfbusiness = models.wf_business.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'userinfo':userinfo,
           'usergroup':usergroup,'login_user': userDict['user'],'status':'', }
    print(msg)
    return render_to_response('workflow/wfbusiness_add.html',msg)


def wfbusinessForm_update(request,*args,**kwargs):
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
def wfbusinessForm_deploy(request,*args,**kwargs):
    git_url = 'http://10.180.11.8'
    git_token = 'F7nAGXozy4dsfJvxiLu_'
    git_tools = gitlab.Gitlab(git_url,git_token)
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
    hostInfo = models.hostInfo.objects.all()
    scriptType = models.scriptType.objects.all()
    print(scriptType,type(scriptType))
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功',
           'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,
           'branches':branches,'tags':tags,'hostInfo':hostInfo,
           'scriptType':scriptType}
    print(msg)
    return render_to_response('workflow/wfbusiness_deploy.html',msg)


def wfbusiness_deploy_query(job,name,proj_id,repo,branch,tag,opertator,update_time,):
    state=job.state
    if state == 'PENDING':
        pass
    else:
        models.wf_business_deploy_history.objects.last().update(state=state)
    #return result
    return state
    #print(state)


@outer
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

    job = tasks.deploy.s(host, port, username, password, command).delay()
    state = job.state
    #print(job,job.status,job.result)
    models.wf_business_deploy_history.objects.create(name=name, proj_id=proj_id, repo=repo,
                                                     branch=branch, tag=tag, opertator=opertator,
                                                     update_time=update_time, state=state)
    t= loop.LoopTimer(3,wfbusiness_deploy_query,[job,name,proj_id,repo,branch,tag,opertator,update_time,])
    t.start()
    msg = {'id':id, 'login_user':userDict['user'],'wfbusiness':wfbusiness,'userinfo':userinfo,'usergroup':usergroup,
           'hostInfo':hostInfo,'scriptType':scriptType,'status':'','login_user': userDict['user'],}
    #print(msg)
    return redirect('/cmdb/index/wf/wfbusiness/deploy/list/',msg)

@outer
def wfbusiness_deploy_list(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    wfbusiness = models.wf_business_deploy_history.objects.all()
    msg = {'wfbusiness':wfbusiness,'login_user': userDict['user'],}
    return render_to_response('workflow/wfbusiness_deploy_result.html',msg)

@outer
def wfbusinessAdd(request,*args,**kwargs):
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
def wfbusiness(request,*args,**kwargs):
    wfbusiness=models.wf_business.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wfbusiness': wfbusiness, 'login_user': userDict['user'],}
    return render_to_response('workflow/wfbusiness.html',msg)

@outer
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

def wfbusinessDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.wf_business.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除工单类型id:'+id,}
    return render_to_response('workflow/wfbusiness.html',msg)

def wfbusinessUpdate(request,*args,**kwargs):
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

@outer
def wf(request,*args,**kwargs):

    wf_info = models.wf_info.objects.all()
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'login_user': userDict['user'], 'wf_info': wf_info,'userinfo':userinfo,}
    '''
    # Load the workflow specification:
    with open('myapp/wf.py') as fp:
        serializer = XmlSerializer()
        spec = WorkflowSpec.deserialize(serializer, fp.read())

    # Create an instance of the workflow, according to the specification.
    wf = Workflow(spec)

    # Complete tasks as desired. It is the job of the workflow engine to
    # guarantee a consistent state of the workflow.
    wf.complete_task_from_id(...)

    # Of course, you can also persist the workflow instance:
    #xml = wf.serialize(XmlSerializer, 'workflow/workflow_state.xml')
    '''
    return render_to_response('workflow/workflow.html',msg)

@outer
def wrokflow_form_add(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    user_group = models.userGroup.objects.all()
    user_info = models.userInfo.objects.all()
    wf_business = models.wf_business.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method=='GET':
        msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status':'', 'wf_type':wf_type,
               'user_info':user_info,'user_group':user_group,'wf_business':wf_business}
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

@outer
def workflow_add(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    userinfo = models.userInfo.objects.all()
    user_group = models.userGroup.objects.all()

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
            approval_id = request.POST.get('approval', None)
            try:
                approval_select = models.userInfo.objects.get(id=approval_id,)
            except:
                approval_select = None
            is_empty = all([title,content,type_select,approval_select,wfbusiness_select,])
            if is_empty:
                # email = models.userInfo.objects.filter(id=approval_id).values('email')[0]['email']
                # username = models.userInfo.objects.filter(id=approval_id).values('username')[0]['username']
                models.wf_info.objects.create(sn=sn, title=title, sponsor=sponsor, type=type_select,
                 content=content, approval=approval_select, memo=memo,business=wfbusiness_select, )
                #models.wf_info.objects.create(sn=sn, title=title, sponsor=sponsor, type=type_select,
                #                              content=content, memo=memo,
                #                              business=wfbusiness_select, )
                # print(type_select,approval_select,email,username,)
                # return render_to_response('workflow/workflow.html',msg)
                # tasks.send_email_workflow.delay(email, username, sn,)
                #print(workflow.NuclearStrikeWorkflowSpec())
                return redirect('/cmdb/index/wf/requests/list/')
            else:
                status = '带有*的选项不能为空！'
                msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'error': status,
                       'wf_type': wf_type, 'userinfo': userinfo, }
                return render_to_response('workflow/500.html',msg)

@outer
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
            approval = models.userInfo.objects.filter(wf_info__sn=sn)
            #update_time = timezone.now()
            #update_time = obj.update(update_time=update_time)
            #print(update_time,type(update_time))
            userDict = request.session.get('is_login', None)
            msg = {'id':id,'sn':sn,'title':title,'sponsor':sponsor,'type':type,'login_user':userDict['user'],
                   'status':'操作成功','approval':approval,
                   'content':content,'memo':memo,'business':business}
            print(msg)
            print(approval,)
            return render_to_response('workflow/workflow_update.html',msg)


@outer
def workflow_update(request,*args,**kwargs):
    try:
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        sponsor = request.POST.get('sponsor')
        type = request.POST.get('type', None)
        type_select = models.wf_type.objects.get(name=type)
        approval = request.POST.get('approval', None)
        approval_select = models.userInfo.objects.get(username=approval)
        title = request.POST.get('title')
        content = request.POST.get('content')
        memo = request.POST.get('memo')
        update_time = timezone.now()
        print(id,sponsor,type,content,approval,memo,)
        #userDict = request.session.get('is_login', None)
        models.wf_info.objects.filter(sn=sn).update(title=title,sponsor=sponsor,type=type_select,
              content=content,approval=approval_select,update_time=update_time,)
        return render_to_response('workflow/workflow_update.html')
    except Exception as e:
        print(e,)
    finally:
        return redirect('/cmdb/index/wf/requests/list/')

@outer
def workflow_detail(request,*args,**kwargs):
    sn = request.GET.get('sn',None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_info_commit = models.wf_info_history_commit.objects.filter(sn=sn)
    wf_info_process = models.wf_info_history_process.objects.filter(sn=sn)
    wf_info_complete = models.wf_info_history_complete.objects.filter(sn=sn)
    approval_selected_id = wf_info.values('approval')[0]['approval']
    approval_selected = models.userInfo.objects.filter(id=approval_selected_id)
    approval = models.userInfo.objects.all()
    approval_set = approval_selected & approval
    wf_type = models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status': '','wf_type': wf_type,
           'approval_selected':approval_selected,'approval':approval,'approval_set':approval_set,
           'wf_info_commit':wf_info_commit,'wf_info_process':wf_info_process,'wf_info_complete':wf_info_complete}
    return render_to_response('workflow/workflow_detail.html',msg)

@outer
def workflow_approve(request,*args,**kwargs):
    sn = request.GET.get('sn',None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_info_commit = models.wf_info_history_commit.objects.filter(sn=sn)
    wf_info_process = models.wf_info_history_process.objects.filter(sn=sn)
    wf_info_complete = models.wf_info_history_complete.objects.filter(sn=sn)
    approval_selected_id = wf_info.values('approval')[0]['approval']
    approval_selected = models.userInfo.objects.filter(id=approval_selected_id)
    approval = models.userInfo.objects.all()
    approval_set = approval_selected & approval
    wf_type = models.wf_type.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'wf_info': wf_info, 'login_user': userDict['user'],'status': '','wf_type': wf_type,
           'approval_selected':approval_selected,'approval':approval,'approval_set':approval_set,
           'wf_info_commit':wf_info_commit,'wf_info_process':wf_info_process,'wf_info_complete':wf_info_complete}
    return render_to_response('workflow/workflow_approve.html',msg)

@outer
def workflow_tasks(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    assignee = userDict['user']
    approval_id = models.userInfo.objects.get(username=userDict['user'])
    wf_info = models.wf_info.objects.filter(approval_id=approval_id).filter(flow_id__gt=0).filter(~Q(status='已完成'))
    number = wf_info.count()
    wf_info_process = models.wf_info_history_process.objects.filter(assignee=assignee)
    number_process = wf_info_process.count()
    wf_type = models.wf_type.objects.all()
    msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': '',
           'wf_type': wf_type,'wf_info_process':wf_info_process,'number':number,'number_process':number_process}
    print(msg,)
    return render_to_response('workflow/workflow_tasks.html',msg)


@outer
def workflow_requests(request,*args,**kwargs):
    userDict = request.session.get('is_login', None)
    wf_info = models.wf_info.objects.filter(sponsor=userDict['user'])
    wf_type = models.wf_type.objects.all()
    msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': '',
           'wf_type': wf_type, }
    print(msg, )
    return render_to_response('workflow/workflow_requests.html', msg)

@outer
def workflow_commit(request,*args,**kwargs):
    if request.method=='GET':
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        if status != "未提交":
            msg = {'error':'流程进行中，不能重复提交！'}
            return render_to_response('workflow/500.html',msg)
        else:
            approval_selected_id = wf_info.values('approval')[0]['approval']
            approval_selected = models.userInfo.objects.filter(id=approval_selected_id)
            email = approval_selected.values('email')[0]['email']
            username = approval_selected.values('username')[0]['username']
            #g = group(tasks.workflow_commit.s(sn),tasks.send_email_workflow.s(email, username,sn,)).delay()
            c1 = tasks.workflow_commit.apply_async((sn,),link=tasks.workflow_send_email.s(username,email))
            userDict = request.session.get('is_login', None)
            msg = {'wf_info': wf_info, 'login_user': userDict['user'],
                    'status': '',}
            #print(sn,email)
            #res = tasks.send_email_workflow.s(email, username,sn,).delay()
            #print(res.get())
            #return render_to_response('workflow/workflow.html',msg)
            #print(g.get(),g.ready(),g.successful(),)
            print(list(c1.collect()),c1.children,c1.get(),)
            return redirect('/cmdb/index/wf/requests/list/',msg)

@outer
def workflow_withdraw(request,*args,**kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        if status != "未提交":
            msg = {'error':'流程进行中，不能撤回！'}
            return render_to_response('workflow/500.html',msg)
        else:
            status = '已撤销'
            approval_selected_id = wf_info.values('approval')[0]['approval']
            approval_selected = models.userInfo.objects.filter(id=approval_selected_id)
            email = approval_selected.values('email')[0]['email']
            username = approval_selected.values('username')[0]['username']
            update_time = timezone.now()
            flow_id = -1
            wf_info.update(status=status, update_time=update_time, flow_id=flow_id)
            type_id = wf_info.values('type')[0]['type']
            try:
                business = models.wf_business.objects.get(wf_info__sn=sn)
                type = models.wf_type.objects.get(wf_info__sn=sn)
            except:
                business = None
                type = None
            sponsor = wf_info.values('sponsor')[0]['sponsor']
            title = wf_info.values('title')[0]['title']
            content = wf_info.values('content')[0]['content']
            models.wf_info_history_withdraw.objects.create(sn=sn, title=title, sponsor=sponsor, type_id=type_id,
                       approval_id=approval_selected_id, content=content, status=status, business=business)
            userDict = request.session.get('is_login', None)
            msg = {'wf_info': wf_info, 'login_user': userDict['user'],
                    'status': '', }
            print(sn, email)
            #res = tasks.send_email_workflow.s(email, username, sn, ).delay()
            #print(res.get())
            # return render_to_response('workflow/workflow.html',msg)
            return redirect('/cmdb/index/wf/requests/list/', msg)

@outer
def workflow_upload(request,*args,**kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    user_group = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        files = request.FILES.get('mf', None)
        print(files, )
        if not files:
            status = '没有文件上传'
            msg = {'wf_info': wf_info, 'login_user': userDict['user'], 'status': status,
                   'wf_type': wf_type, 'user_group': user_group, }
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



def workflow_process(request,*args,**kwargs):
    if request.method=='POST':
        suggest = request.POST.get('suggest',None)
        suggest_agree=request.POST.get('suggest_agree',None)
        suggest_reject = request.POST.get('suggest_reject', None)
        username_sponsor = request.POST.get('sponsor',None)
        email_sponsor = models.userInfo.objects.filter(username=username_sponsor).values('email')[0]['email']
        sn = request.POST.get('sn', None)
        title = request.POST.get('title',None)
        content = request.POST.get('content', None)
        type = request.POST.get('type',None)
        #type_id = models.wf_type.objects.get(name=type)
        #approval_id = request.POST.get('approval')
        #approval = models.userInfo.objects.filter(id=approval_id)
        #username_approval = approval.values('username')[0]['username']
        #email_approval = approval.values('email')[0]['email']
        userDict = request.session.get('is_login', None)
        assignee = userDict['user']
        #print(sn, username_sponsor,email_sponsor,username_approval,email_approval,
        #        suggest,suggest_agree,suggest_reject)
        wf_info = models.wf_info.objects.filter(sn=sn)
        business_id = wf_info.values('business')[0]['business']
        wf_business = models.wf_business.objects.filter(id=business_id)
        group_id = wf_business.values('group')[0]['group']
        approval = models.userInfo.objects.filter(group_id=group_id).filter(approval='1')
        approval_ins = models.userInfo.objects.filter(group_id=group_id).get(approval='1')
        username_approval = approval.values('username')[0]['username']
        email_approval = approval.values('email')[0]['email']
        # wf_type = models.wf_type.objects.all()
        type_id = models.wf_type.objects.get(name=type)
        wf_type = models.wf_type.objects.all()
        flow_id = wf_info.values('flow_id')[0]['flow_id']  # 第一次提交flow_id值为1

        if suggest=='同意':

            flow_id = flow_id+1  # 每次处理flow_id值加1

            suggest_agree = request.POST.get('suggest_agree', None)
            #res = tasks.workflow_send_email.s().delay(sn,username_approval,email_approval,)
            #return res
            #print(res, res.status, res.id, type(res), res.result, res.date_done)
            #print(res.request.id,res.name,)
            #cache.set(res,res.id)
            #cache.get(res)

            if flow_id < 3:
                c2 = tasks.workflow_process.apply_async(
                    (sn, title, username_sponsor, type, content, suggest, suggest_agree, assignee,suggest_reject,flow_id),
                    link=tasks.workflow_send_email.s(username_approval, email_approval))
                print(list(c2.collect()), c2.children, c2.get(), )
            else:
                c2 = tasks.workflow_process.apply_async(
                    (sn, title, username_sponsor, type, content, suggest, suggest_agree, assignee, suggest_reject,flow_id),
                    link=tasks.workflow_send_email.s(username_sponsor, email_sponsor))
                print(list(c2.collect()), c2.children, c2.get(),)

            msg = {'wf_info': wf_info, 'login_user': userDict['user'],
                  'status': '', 'wf_type': wf_type,}
            #print(res,type(res))
            #print(type,type_id,)
            #return render_to_response('workflow/workflow_tasks.html', msg)
            return redirect('/cmdb/index/wf/tasks/list/')


        if suggest=='拒绝':

            flow_id = flow_id+1  # 每次处理flow_id值加1

            suggest_reject=request.POST.get('suggest_reject',None)
            #res = tasks.send_email_workflow.s().delay(email_sponsor, username_sponsor, sn,)
            #print(res, res.status, res.id, type(res), res.result, res.date_done)
            #print(res.request.id)
            c3 = tasks.workflow_process.apply_async(
                (sn, title, username_sponsor, type, content, suggest, suggest_agree, assignee, suggest_reject,flow_id),
                link=tasks.workflow_send_email.s(username_sponsor, email_sponsor))
            print(list(c3.collect()), c3.children, c3.get(), )
            msg = {'wf_info': wf_info, 'login_user': userDict['user'],
                   'status': '', 'wf_type': wf_type, }
            #print(res,type(res),)   ###TypeError: 'str' object is not callable
            return redirect('/cmdb/index/wf/tasks/list/')

