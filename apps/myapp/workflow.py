#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from apps.myapp.auth_helper import custom_login_required, custom_permission_required, secret_required
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from apps.myapp import models
from django.shortcuts import redirect
from apps.myapp import tasks
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
from django.core.cache import cache
from django.contrib.auth.models import Group
from apps.myapp import common
from apps.myapp import page_helper
from apps.myapp import json_helper
from celery.result import AsyncResult
from myweb.settings import *


@custom_login_required
@custom_permission_required('myapp.view_wf_business')
def wfbusiness(request, *args, **kwargs):
    wfbusiness = models.wf_business.objects.all()
    count = wfbusiness.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wfbusiness': wfbusiness, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/wfbusiness.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def wfbusiness_form_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    wfbusiness = models.wf_business.objects.all()
    # usergroup = models.userGroup.objects.all()
    approval = userinfo.exclude(workflow_order=0)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wfbusiness': wfbusiness, 'userinfo': userinfo,
           'login_user': user_dict['user'], 'status': '', 'approval': approval,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('workflow/wfbusiness_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def wfbusiness_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        wfbusiness = request.POST.get('wfbusiness', None)
        repo = request.POST.get('repo', None)
        admin_id = request.POST.get('admin', None)
        approval = request.POST.getlist('approval', None)
        is_exist = models.wf_business.objects.filter(name=wfbusiness)
        # print(is_exist)
        if not is_exist:
            is_empty = all([wfbusiness, ])
            if is_empty:
                queryset = models.wf_business.objects.create(name=wfbusiness, admin_id=admin_id, )
                queryset.approval.set(approval)
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': user_dict['user'], 'status': '添加业务单元成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/wf/wfbusiness/list/')
            else:
                msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                       'login_user': user_dict['user'], 'status': 'xx不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'userinfo': userinfo, 'wfbusiness': wfbusiness,
                   'login_user': user_dict['user'], 'status': '该业务单元已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/wfbusiness_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusiness_form_update(request, *args, **kwargs):
    id = kwargs['id']
    wfbusiness = models.wf_business.objects.filter(id=id)
    admin = models.userInfo.objects.all().exclude(admin__id=id)
    approval = models.userInfo.objects.all().exclude(workflow_order=0).exclude(approval__id=id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': id, 'login_user': user_dict['user'], 'status': u'操作成功', 'wfbusiness': wfbusiness,
           'admin': admin, 'approval': approval, 'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('workflow/wfbusiness_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusiness_update(request, *args, **kwargs):
    id = kwargs['id']
    # 2023/08/18
    '''
    wfbusiness_id = request.POST.get('wfbusiness')
    wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id).values('name')[0]['name']
    '''
    wfbusiness = request.POST.get('wfbusiness')
    admin_id = request.POST.get('admin')
    approval = request.POST.getlist('approval')

    update_time = timezone.now()
    user_dict = request.session.get('is_login', None)
    models.wf_business.objects.filter(id=id).update(name=wfbusiness,
                                                    update_time=update_time, admin_id=admin_id, )
    models.wf_business.objects.get(id=id).approval.set(approval)
    return redirect('/cmdb/index/wf/wfbusiness/list/')


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def wfbusiness_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            wfbusiness_id = request.POST.get('wfbusiness', None)
            print(wfbusiness_id)
            wfbusiness = models.wf_business.objects.filter(id=wfbusiness_id)
            director_id = wfbusiness.values('director_id')[0]['director_id']
            director = models.userInfo.objects.filter(id=director_id).values('username')[0]['username']
            print(wfbusiness, director_id, director, )
            user_dict = request.session.get('is_login', None)
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
@custom_permission_required('myapp.delete_wf_business')
def wfbusiness_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.wf_business.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除业务单元成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('workflow/wfbusiness.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_type')
def wftype(request, *args, **kwargs):
    wftype = models.wf_type.objects.all()
    count = wftype.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wftype': wftype, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/wftype.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_type')
def wftypeForm_add(request, *args, **kwargs):
    # userinfo = models.userInfo.objects.all()
    wftype = models.wf_type.objects.all()
    # usergroup = models.userGroup.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wftype': wftype, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/wftype_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_type')
def wftypeAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    # usertype = models.userType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # usergroup = models.userGroup.objects.all()
    # result = {'status': '','usertype':None}
    if request.method == 'POST':
        wftype = request.POST.get('wftype', None)
        is_exist = models.wf_type.objects.filter(name=wftype)
        # print(is_exist)
        if not is_exist:
            is_empty = all([wftype, ])
            if is_empty:
                models.wf_type.objects.create(name=wftype, )
                msg = {'userinfo': userinfo, 'wftype': wftype,
                       'login_user': user_dict['user'], 'status': '添加工单类型成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/wf/wftype/list/')
            else:
                msg = {'userinfo': userinfo, 'wftype': wftype,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'userinfo': userinfo, 'wftype': wftype,
                   'login_user': user_dict['user'], 'status': '该工单类型已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/wftype_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_type')
def wftypeForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    wftype = models.wf_type.objects.filter(id=id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': id, 'login_user': user_dict['user'], 'status': '操作成功', 'wftype': wftype,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('workflow/wftype_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_type')
def wftypeUpdate(request, *args, **kwargs):
    id = kwargs['id']
    wftype = request.POST.get('wftype')
    update_time = timezone.now()
    user_dict = request.session.get('is_login', None)
    models.wf_type.objects.filter(id=id).update(name=wftype, update_time=update_time)
    return redirect('/cmdb/index/wf/wftype/list/')


@custom_login_required
@custom_permission_required('myapp.delete_wf_type')
def wftype_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.wf_type.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除工单类型成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('workflow/wftype.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def wf(request, *args, **kwargs):
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    count = models.wf_info.objects.all().count()
    pageinfo = page_helper.pageinfo(page, count, perItem)
    # 工单列表降序排列
    wf_info = models.wf_info.objects.all().order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_wf_list(request, page, pageinfo.pageCount)
    # usertype = userType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wf_info': wf_info, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': user_dict['user'],
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/workflow.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def wf_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/wf/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/wf/list/')


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def wf_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    wf_info = models.wf_info.objects.filter(sn__icontains=keyword) | models.wf_info.objects.filter(
        sponsor__icontains=keyword)
    count = wf_info.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    wf_info = wf_info.order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_wf_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('workflow/workflow.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_info')
def wrokflow_form_add(request, *args, **kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    # user_group = models.userGroup.objects.all()
    user_info = models.userInfo.objects.all()
    wf_business = models.wf_business.objects.all()
    # 2023/08/15
    deploy_list = models.deploy_app.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'GET':
        msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '', 'wf_type': wf_type,
               'user_info': user_info, 'wf_business': wf_business, 'deploy_list': deploy_list,
               'wf_count_pending': wf_dict['wf_count_pending'], }
        # print(msg, )
        return render_to_response('workflow/workflow_add.html', msg)
    if request.method == 'POST':

        '''
        dest=open(os.path.join("F:\\upload",import),'wb+')
        for chunk in import.chunks():
            dest.write(chunk)
        dest.close()
        '''

        '''
        path = default_storage.save('temp/dj', ContentFile(import.read()))
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
            mf = request.FILES.get('mf')
            print(mf, type(mf), )
            print(mf.read, )
            fileName = request.POST.get('fileName')
            print(fileName, type(fileName), )
            uploadDir = 'C:/upload/'
            if not os.path.exists(uploadDir):
                os.mkdir(uploadDir)
            fileName = uploadDir + fileName
            with open(fileName, 'wb+', ) as f:
                for chunk in mf:
                    f.write(chunk)
            status = '上传完成'
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': status,
                   'wf_type': wf_type, }
            # print(msg, )
            return render_to_response('workflow/workflow_add.html', msg)
        except Exception as e:
            print('error:', e)


@custom_login_required
@custom_permission_required('myapp.add_wf_info')
def workflow_add(request, *args, **kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
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
        wfbusiness_id = request.POST.get('wf_business', None)
        # print(wfbusiness_id)
        try:
            wfbusiness_select = models.wf_business.objects.get(id=wfbusiness_id)
        except:
            wfbusiness_select = None

        # print(title, content, type_select, wfbusiness_select)

        # 2023/12/01 判断是否为‘生产发布’类型工单请求，生产发布：id=1
        if type_id == '1':
            # 2023/08/16
            proj_name_id = request.POST.get('proj_name', None)
            proj_tag = request.POST.get('proj_tag', None)
            if proj_name_id is not None:
                proj_name = models.deploy_app.objects.filter(id=proj_name_id).values('proj_name')[0]['proj_name']
                proj_id = models.deploy_app.objects.filter(id=proj_name_id).values('proj_id')[0]['proj_id']

            else:
                proj_name = None
                proj_id = None
            is_empty = all([title, content, type_select, wfbusiness_select, sponsor, proj_name, proj_tag, proj_id])
        else:
            proj_name = None
            proj_id = None
            proj_tag = None
            is_empty = all([title, content, type_select, wfbusiness_select, sponsor])

        if is_empty:
            models.wf_info.objects.create(sn=sn, title=title, sponsor=sponsor, type=type_select,
                                          content=content, memo=memo, business=wfbusiness_select,
                                          proj_name=proj_name,
                                          proj_tag=proj_tag, proj_id=proj_id)
            return redirect('/cmdb/index/wf/requests/list/')
        else:
            status = '带有*的选项不能为空！'
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': status,
                   'wf_type': wf_type, 'userinfo': userinfo, }
            return render_to_response('500.html', msg, status=500)
    else:
        status = '请使用post提交请求！'
        msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'error': status,
               'wf_type': wf_type, 'userinfo': userinfo, 'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=405)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_form_update(request, *args, **kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        obj = models.wf_info.objects.filter(sn=sn)
        status = obj.values('status')[0]['status']
        if status == "已提交":
            msg = {'status': '流程进行中，不能修改！'}
            return render_to_response('500.html', msg, status=500)
        elif status == "已完成":
            msg = {'status': '流程已结束，不能修改！'}
            return render_to_response('500.html', msg, status=500)
        else:
            title = obj.values('title')
            sponsor = obj.values('sponsor')
            business = models.wf_business.objects.filter(wf_info__sn=sn)
            type = models.wf_type.objects.filter(wf_info__sn=sn)
            content = obj.values('content')
            memo = obj.values('memo')
            user_dict = request.session.get('is_login', None)
            wf_dict = request.session.get('wf', None)
            # 2023/08/16
            try:
                proj_name_selected = obj.values('proj_name')[0]['proj_name']
                proj_tag_selected = obj.values('proj_tag')[0]['proj_tag']
                git_tools = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN)
                proj_id = models.deploy_app.objects.filter(proj_name=proj_name_selected).values('proj_id')[0]['proj_id']
                proj = git_tools.projects.get(proj_id)
                tags = proj.tags.list()
            except Exception as e:
                proj_name_selected = None
                proj_tag_selected = None
                tags = None
                print(e)

            deploy_list = models.deploy_app.objects.all()

            msg = {'id': id, 'sn': sn, 'title': title, 'sponsor': sponsor, 'type': type,
                   'login_user': user_dict['user'],
                   'status': '操作成功', 'proj_name_selected': proj_name_selected,
                   'proj_tag_selected': proj_tag_selected, 'wf_count_pending': wf_dict['wf_count_pending'],
                   'deploy_list': deploy_list, 'tags': tags, 'content': content, 'memo': memo, 'business': business}
            # print(msg)
            return render_to_response('workflow/workflow_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_update(request, *args, **kwargs):
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
        # 20230816
        proj_name = request.POST.get('proj_name', None)
        proj_tag = request.POST.get('proj_tag', None)

        # print(id, sponsor, type, content, memo, )
        # print(proj_name, proj_tag)
        try:
            proj_id = models.deploy_app.objects.filter(proj_name=proj_name).values('proj_id')[0]['proj_id']
        except:
            proj_id = None
        # print(proj_id, )
        # userDict = request.session.get('is_login', None)
        models.wf_info.objects.filter(sn=sn).update(title=title, sponsor=sponsor, type=type_select,
                                                    content=content, memo=memo, update_time=update_time,
                                                    proj_name=proj_name, proj_tag=proj_tag, proj_id=proj_id)
        return render_to_response('workflow/workflow_update.html')
    except Exception as e:
        print(e, )
    finally:
        return redirect('/cmdb/index/wf/requests/list/')


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
def workflow_detail(request, *args, **kwargs):
    sn = request.GET.get('sn', None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    wf_info_process_start = models.wf_info_process_history.objects.filter(sn=sn).filter(status='已提交')
    wf_info_process = models.wf_info_process_history.objects.filter(sn=sn).exclude(status='已提交').exclude(
        status='已完成').order_by('flow_id')
    wf_info_process_end = models.wf_info_process_history.objects.filter(sn=sn).filter(status='已完成')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '',
           'wf_info_process_start': wf_info_process_start, 'wf_info_process': wf_info_process,
           'wf_info_process_end': wf_info_process_end, 'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/workflow_detail.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
def workflow_approve(request, *args, **kwargs):
    sn = request.GET.get('sn', None)
    wf_info = models.wf_info.objects.filter(sn=sn)
    next_assignee_username = wf_info.values('next_assignee')[0]['next_assignee']
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    login_user = user_dict['user']
    # 2023/09/20 判断流程当前状态
    wf_status = wf_info.values('status')[0]['status']
    if wf_status != '已完成':
        # 2023/09/06 判断当前登录用户是否为审批人
        if login_user == next_assignee_username:
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('workflow/workflow_approve.html', msg)
        else:
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'],
                   'status': '前登录用户不是当前流程的审批人，请切换用户再试！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=500)
    else:
        msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '此流程已结束！',
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=500)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_tasks_status(request, *args, **kwargs):
    sn = request.POST.get('sn', None)
    # print(sn,type(sn),)
    task_status = models.wf_info.objects.filter(sn=sn).values('status')[0]['status']
    msg = {'status': task_status, 'sn': sn, }
    return HttpResponse(json.dumps(msg))


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_tasks(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)

    count_pending = models.wf_info.objects.filter(next_assignee=user_dict['user']).filter(flow_id__gte=0).filter(
        ~Q(status='已完成')).count()
    count_processing = models.wf_info_process_history.objects.filter(assignee=user_dict['user']).filter(
        flow_id__gt=0).count()

    pageinfo_pending = page_helper.pageinfo(page, count_pending, perItem)
    pageinfo_processing = page_helper.pageinfo(page, count_processing, perItem)

    # 工单列表降序排列
    wf_info = models.wf_info.objects.filter(next_assignee=user_dict['user']).filter(flow_id__gte=0).filter(
        ~Q(status='已完成')).order_by('-id')[pageinfo_pending.start:pageinfo_pending.end]

    wf_info_process = models.wf_info_process_history.objects.filter(assignee=user_dict['user']).filter(
        flow_id__gt=0).order_by('-id')
    # 2023/11/27
    # queryset转为list
    # print(list(wf_info_process))
    # print(wf_info_process)
    # 从流程历史sn查找当前流程状态
    wf_info_process_new = models.wf_info.objects.filter(sn__in=[x.sn for x in wf_info_process]).order_by('-id')[
                          pageinfo_processing.start:pageinfo_processing.end]
    # print(wf_info_process_new)
    wf_type = models.wf_type.objects.all()

    page_string_pending = page_helper.pager_wf_task_list(request, page, pageinfo_pending.pageCount)
    page_string_processing = page_helper.pager_wf_task_list(request, page, pageinfo_processing.pageCount)

    msg = {'wf_info': wf_info, 'wf_info_process': wf_info_process, 'login_user': user_dict['user'], 'status': '',
           'wf_type': wf_type, 'count_pending': count_pending, 'count_processing': count_processing,
           'wf_info_process_new': wf_info_process_new, 'page_pending': page_string_pending,
           'page_processing': page_string_processing, 'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg,)
    return render_to_response('workflow/workflow_tasks.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_requests(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    wf_type = models.wf_type.objects.all()
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)

    count = models.wf_info.objects.filter(sponsor=user_dict['user']).count()
    pageinfo = page_helper.pageinfo(page, count, perItem)
    # 工单列表降序排列
    wf_info = models.wf_info.objects.filter(sponsor=user_dict['user']).order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_wf_request_list(request, page, pageinfo.pageCount)

    msg = {'wf_info': wf_info, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': user_dict['user'], 'wf_type': wf_type,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('workflow/workflow_requests.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_requests_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/wf/requests/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/wf/requests/list/')


@custom_login_required
@custom_permission_required('myapp.view_wf_info')
@custom_permission_required('myapp.view_wf_info_process_history')
def workflow_requests_search_result(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    keyword = kwargs['keyword']
    wf_info = models.wf_info.objects.filter(sponsor=user_dict['user']).filter(
        sn__icontains=keyword) | models.wf_info.objects.filter(
        sponsor=user_dict['user']).filter(title__icontains=keyword)
    count = wf_info.count()
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    wf_info = wf_info.order_by('-id')[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_wf_request_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('workflow/workflow_requests.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_commit(request, *args, **kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        user_dict = request.session.get('is_login', None)
        wf_dict = request.session.get('wf', None)
        wf_info = models.wf_info.objects.filter(sn=sn)
        status = wf_info.values('status')[0]['status']
        if status == "已提交":
            msg = {'status': '流程进行中，不能提交！'}
            return render_to_response('500.html', msg, status=500)
        elif status == "已完成":
            msg = {'status': '流程已结束，不能提交！'}
            return render_to_response('500.html', msg, status=500)
        else:
            # c1 = tasks.workflow_commit.apply_async((sn,), link=tasks.workflow_send_email.s(username, email))
            # print(list(c1.collect()),c1.children,c1.get(),)
            tasks.workflow_commit(sn)
            '''
            # 2023/08/17
            proj_name = wf_info.values('proj_name')[0]['proj_name']
            proj_tag = wf_info.values('proj_tag')[0]['proj_tag']
            proj_id = wf_info.values('proj_id')[0]['proj_id']
            business_id = wf_info.values('business')[0]['business']
            unit = models.wf_type.objects.filter(id=business_id).values('name')[0]['name']
            deploy_status = '已提交'
            max_id = models.deploy_list_detail.objects.all().order_by('-id')[0].id
            if max_id is None:
                # 如果数据库为空，则从 ID 为 1 的数据开始提取
                max_id = 0
            print(max_id, type(max_id))
            ######################################
            # 2023/08/17
            task_id = tasks.ssh_remote.delay(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD,
                             SSH_CMD + ' ' + proj_id + ' ' + proj_name + ' ' + proj_tag + ' ' + str(max_id + 1))
            print(task_id)
            models.deploy_list_detail.objects.create(unit=unit, proj_name=proj_name, proj_id=proj_id,
                                                     tag=proj_tag, task_id=task_id, status=deploy_status)
            ##################
            '''
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return redirect('/cmdb/index/wf/requests/list/', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_withdraw(request, *args, **kwargs):
    if request.method == 'GET':
        sn = kwargs['sn']
        wf_info = models.wf_info.objects.filter(sn=sn)
        flow_id = wf_info.values('flow_id')[0]['flow_id']
        if flow_id > 0:
            msg = {'status': '流程进行中，不能撤回！'}
            return render_to_response('500.html', msg, status=500)
        elif flow_id < 0:
            msg = {'status': '流程未提交，不需要撤回！'}
            return render_to_response('500.html', msg, status=500)
        else:
            tasks.workflow_withdraw(sn)
            user_dict = request.session.get('is_login', None)
            wf_dict = request.session.get('wf', None)
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': '',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return redirect('/cmdb/index/wf/requests/list/', msg)


@custom_login_required
def workflow_upload(request, *args, **kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    # user_group = models.userGroup.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        files = request.FILES.get('mf', None)
        # print(import, )
        if not files:
            status = '没有文件上传'
            msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': status,
                   'wf_type': wf_type, }
            print(msg, )
            return render_to_response('workflow/workflow_add.html', msg)
        '''
        dest=open(os.path.join("F:\\upload",import),'wb+')
        for chunk in import.chunks():
            dest.write(chunk)
        dest.close()
        '''
        path = default_storage.save('temp/dj', ContentFile(files.read()))
        # temp_file = os.path.join(settings.MEDIA_ROOT, path)
        status = '上传完成'
        msg = {'wf_info': wf_info, 'login_user': user_dict['user'], 'status': status,
               'wf_type': wf_type, 'user_group': user_group,
               'status': '', 'wf_count_pending': wf_dict['wf_count_pending'], }
        # print(msg, )
        return render_to_response('workflow/workflow_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_info')
@custom_permission_required('myapp.change_wf_info_process_history')
def workflow_process(request, *args, **kwargs):
    if request.method == 'POST':
        suggest = request.POST.get('suggest', None)
        suggest_agree = request.POST.get('suggest_agree', None)
        suggest_reject = request.POST.get('suggest_reject', None)
        sn = request.POST.get('sn', None)
        wf_info = models.wf_info.objects.filter(sn=sn)
        user_dict = request.session.get('is_login', None)
        # wf_dict = request.session.get('wf', None)
        tasks.workflow_process(sn, suggest, suggest_agree, suggest_reject)
        # 2024/5/6  更新session待办信息
        wf_count_pending = models.wf_info.objects.filter(next_assignee=user_dict['user']).filter(
            flow_id__gte=0).filter(
            ~Q(status='已完成')).count()
        print('wf_count_pending:', wf_count_pending)
        if wf_count_pending > 0:
            # del request.session['wf']
            # 处理完减少一次待办数量，直至为'0'
            request.session['wf'] = {'wf_count_pending': wf_count_pending - 1, }
        wf_dict = request.session.get('wf', None)
        msg = {'wf_info': wf_info, 'login_user': user_dict['user'],
               'status': '', 'wf_count_pending': wf_dict['wf_count_pending'], }
        return redirect('/cmdb/index/wf/tasks/list/')


@custom_login_required
def wftype_change(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            deploy_list_id = request.POST.get('deploy_list_id', None)
            # print(deploy_list_id)

            deploy = models.deploy_app.objects.filter(id=deploy_list_id)
            # print(deploy)
            proj_name = deploy.values('proj_name')[0]['proj_name']
            # print(proj_name)
            proj_id = deploy.values('proj_id')[0]['proj_id']
            # print(proj_id)

            # ansible_base_dir = ANSIBLE_BASE_DIR
            # gitlab_url = GITLAB_URL
            # gitlab_token = GITLAB_TOKEN

            # 数据库获取
            ansible_base_dir = models.SystemConfig.objects.filter(name='default').values('ansible_base_dir')[0][
                'ansible_base_dir']
            gitlab_url = models.SystemConfig.objects.filter(name='default').values('gitlab_url')[0][
                'gitlab_url']
            gitlab_token = models.SystemConfig.objects.filter(name='default').values('gitlab_token')[0][
                'gitlab_token']

            git_tools = gitlab.Gitlab(gitlab_url, gitlab_token)
            proj = git_tools.projects.get(proj_id)
            # print(proj)
            branches = proj.branches.list()
            # print(branches)
            # tags = proj.tags.list()
            tags = proj.tags.list()
            tags_name = []
            for item in tags:
                tags_name.append(item.name)
            # print(type(tags), tags)

            # print(json.dumps(tags))
            user_dict = request.session.get('is_login', None)
            wf_dict = request.session.get('wf', None)
            msg = {'tags_name': tags_name}
            # data = serializers.serialize('json',tags)
            # print(data)
            # print(json.dumps(data))
            # print(type(msg), msg)
            return HttpResponse(json.dumps(msg, cls=json_helper.MyEncoder, indent=4))
            # return render_to_response('workflow/workflow_add.html',msg)
        except Exception as e:
            print(e)
            data = {'deploy': e, }
            return HttpResponse(json.dumps(data))


@custom_login_required
def wf_proj_search(request, *args, **kwargs):
    if request.method == 'POST':
        # proj_name_list = list(models.deploy_app.objects.all().values_list('proj_name', flat=True))
        proj_name_list = list(models.deploy_app.objects.all().values_list('id', 'proj_name', ))
        print(proj_name_list)
        msg = {'proj_name_list': proj_name_list}
        return JsonResponse(msg)


'''
@custom_login_required
def wftypeChange2(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            proj_name = request.POST.get('proj_name', None)
            # print(proj_name)

            deploy = models.deploy_app.objects.filter(proj_name=proj_name)
            # print(deploy)

            proj_id = deploy.values('proj_id')[0]['proj_id']
            # print(proj_id)
            git_tools = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN)
            proj = git_tools.projects.get(proj_id)
            # print(proj)
            branches = proj.branches.list()
            # print(branches)
            # tags = proj.tags.list()
            tags = proj.tags.list()
            tags_name = []
            for item in tags:
                tags_name.append(item.name)
            # print(type(tags), tags)

            # print(json.dumps(tags))
            user_dict = request.session.get('is_login', None)
            wf_dict = request.session.get('wf', None)
            msg = {'tags_name': tags_name}
            # data = serializers.serialize('json',tags)
            # print(data)
            # print(json.dumps(data))
            # print(type(msg), msg)
            return HttpResponse(json.dumps(msg))
            # return render_to_response('workflow/workflow_add.html',msg)
        except Exception as e:
            print(e)
            data = {'tags_name': e, }
            return HttpResponse(json.dumps(data))
'''


# @custom_login_required
# @custom_permission_required('myapp.add_wf_info')
@secret_required
def workflow_add_api(request, *args, **kwargs):
    wf_info = models.wf_info.objects.all()
    wf_type = models.wf_type.objects.all()
    # userDict = request.session.get('is_login', None)
    userinfo = models.userInfo.objects.all()

    if request.method == 'POST':
        sn = token_helper.get_random_uuid()
        title = json.loads(request.body).get('title')
        sponsor = json.loads(request.body).get('sponsor', None)
        memo = json.loads(request.body).get('memo', None)
        type_id = json.loads(request.body).get('type', None)

        try:
            type_select = models.wf_type.objects.get(id=type_id, )
        except:
            type_select = None
            return HttpResponse(json.dumps({"error": "type 参数值错误！"}))

        '''
        #get:instance,filter:QuerySet,Error:
        Cannot assign "<QuerySet [<wf_type: wf_type object (1)>]>": "wf_info.types" must be a "wf_type" instance

        action_id = request.POST.get('action',None)
        action_select = models.wf_action.objects.get(id=action_id,)
        '''
        content = json.loads(request.body).get('content', None)
        wfbusiness_id = json.loads(request.body).get('wf_business', None)
        try:
            wfbusiness_select = models.wf_business.objects.get(id=wfbusiness_id)
        except:
            wfbusiness_select = None
            return HttpResponse(json.dumps({"error": "wf_business 参数值错误！"}))
        # print(title, content, type_select, wfbusiness_select, type_id, type(type_id))

        # 2023/12/01 判断是否为‘生产发布’类型工单请求，生产发布：id=1
        if type_id == '1':
            # 2023/08/16
            # proj_name_id = json.loads(request.body).get('proj_name', None)
            proj_name = json.loads(request.body).get('proj_name', None)
            proj_tag = json.loads(request.body).get('proj_tag', None)

            try:
                # proj_name = models.deploy_app.objects.filter(id=proj_name_id).values('proj_name')[0]['proj_name']
                proj_id = models.deploy_app.objects.filter(proj_name=proj_name).values('proj_id')[0]['proj_id']
            except:
                # proj_name = None
                proj_id = None
                return HttpResponse(json.dumps({"error": "proj_name 参数值错误！"}))
            # is_empty = all([title, content, type_select, wfbusiness_select, sponsor, proj_name_id, proj_tag])
            is_empty = all([title, content, type_select, wfbusiness_select, sponsor, proj_name, proj_tag, proj_id])
        else:
            proj_name = None
            proj_id = None
            proj_tag = None
            is_empty = all([title, content, type_select, wfbusiness_select, sponsor, ])

        if is_empty:
            models.wf_info.objects.create(sn=sn, title=title, sponsor=sponsor, type=type_select,
                                          content=content, memo=memo, business=wfbusiness_select,
                                          proj_name=proj_name,
                                          proj_tag=proj_tag, proj_id=proj_id)
            # return redirect('/cmdb/index/wf/requests/list/')
            tasks.workflow_commit(sn)
            return HttpResponse(json.dumps({"status": "接口请求成功！"}))
        else:
            return HttpResponse(json.dumps({"error": "缺少参数！"}))
    else:
        return HttpResponse(json.dumps({"error": "请使用post提交请求！"}))
