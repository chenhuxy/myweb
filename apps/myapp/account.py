#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.db.models import Q
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect, get_object_or_404
import time
import json

# from django.urls import reverse
from django.utils.safestring import mark_safe
from apps.myapp.models import *
from apps.myapp import common
from apps.myapp import page_helper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.template import context
from apps.myapp import zabbix
from apps.myapp import prometheus
from apps.myapp import encrypt_helper
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
# from myapp import ansible_api
from django.template import loader, RequestContext
from apps.myapp import token_helper
from apps.myapp import tasks
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
# from apps.myapp import workflow,wf
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow.serializer.prettyxml import XmlSerializer
from SpiffWorkflow import Workflow
#  form upload
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string, salted_hmac
from django.contrib.auth.decorators import permission_required

#####################################################################################################################################
from django.shortcuts import render, render_to_response, HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
import urllib
import urllib.parse


# Create your views here.

# 添加index函数，用于返回index.html页面


def cmdb(request):
    return redirect('/cmdb/index/')


def login(request):
    return render_to_response('account/login.html')


def logout(request):
    if request.session.get('is_login'):
        del request.session['is_login']
        obj = redirect('/cmdb/login/')
        obj.delete_cookie('is_login')
        # obj.delete_cookie('user')
        # obj.delete_cookie('pass')
    return redirect('/cmdb/login/')


@custom_login_required
def index(request):
    userinfo = userInfo.objects.all()
    user_count = userInfo.objects.all().count()
    deploy_count = deploy_app.objects.all().count()
    deploy_list_count = deploy_list_detail.objects.all().count()
    wf_count = wf_info.objects.all().count()
    # usertype = userType.objects.all()
    # zabbix_alert_count = zabbix.zabbix_alert_count()
    prometheus_alert_count = prometheus.prometheus_alert_count()

    userDict = request.session.get('is_login', None)
    wf_count_pending = wf_info.objects.filter(next_assignee=userDict['user']).filter(
        flow_id__gte=0).filter(
        ~Q(status='已完成')).count()
    msg = {'userinfo': userinfo, 'login_user': userDict['user'],
           'user_count': user_count, 'deploy_count': deploy_count, 'wf_count': wf_count,
           # 'zabbix_alert_count':zabbix_alert_count,'prometheus_alert_count':prometheus_alert_count,}
           'prometheus_alert_count': prometheus_alert_count, 'deploy_list_count': deploy_list_count,
           'wf_count_pending': wf_count_pending}
    return render_to_response('account/index.html', msg, )


# @csrf_protect
def auth(request, *args, **kwargs):
    msg = {'status': ''}
    if request.method == 'POST':
        username = request.POST.get('user', None)
        password_origin = request.POST.get('pwd', None)
        password = encrypt_helper.md5_encrypt(password_origin)
        # password = make_password(password_origin)
        # check = check_password(password_origin,password)
        user = authenticate(username=username, password=password_origin)
        remember = request.POST.get('remember', None)
        is_empty = all([username, password_origin])
        # print(username, password_origin,remember,is_empty,user,type(user))
        if is_empty:
            if user:
                request.session['is_login'] = {'user': username, 'pass': password, }
                obj = redirect('/cmdb/index/')
                if remember == 'on':
                    obj.set_cookie('is_login', '{"user": username, "pass": password, }', 3600 * 24 * 7, )
                    # obj.set_cookie('user',username,3600*24*7,)
                    # obj.set_cookie('pass',password,3600*24*7,)
                return obj
                # result = {'status':'登录成功！'}
                # return render_to_response('index.html',result)
            else:
                msg = {'status': '用户名密码错误！'}
        else:
            msg = {'status': '用户名或密码不能为空！'}
    else:
        msg = {'status': '无效的请求，请使用post提交！'}
    return render_to_response('account/login.html', msg, )


def register(request, *args, **kwargs):
    msg = {'status': ''}
    if request.method == 'POST':
        username = request.POST.get('user', None)
        password1 = request.POST.get('pwd1', None)
        password2 = request.POST.get('pwd2', None)
        email = request.POST.get('email', None)
        # group = userGroup.objects.filter(name="default")
        is_active = 0
        is_empty = all([username, password1, email])
        if is_empty:
            if password2 == password1:
                is_exist = userInfo.objects.filter(username=username) | userInfo.objects.filter(email=email)
                if not is_exist:
                    '''
                    # 加载模板
                    template = loader.get_template('email.html')
                    # 渲染模板
                    token = token_helper.get_random_uuid()
                    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
                    html_str = template.render({"username": username, 'token': token, })
                    print(html_str, type(html_str))
                    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
                    send_mail('【CMDB测试邮件】', '', '834163059@qq.com',
                              [email], fail_silently=False, html_message=html_str)
                    # 记录 token 对应的邮箱是谁 v  k
                    cache.set(token, email, 600)
                    '''
                    tasks.account_send_email.delay(email, username)
                    # password = encrypt_helper.md5_encrypt(password2)
                    # queryset=userInfo.objects.create(username=username,password=password,
                    #                               email=email,is_active=is_active,)
                    # queryset.group.set(group)
                    queryset = userInfo.objects.create(username=username, email=email, is_active=is_active, )
                    queryset.set_password(password2)  # 设置密码
                    queryset.save()  # 保存
                    msg = {'status': username + ',邮件已发送至' + email + ',请前往邮箱激活!'}
                    return render_to_response('account/register.html', msg)
                else:
                    msg = {'status': '该用户已存在！'}
                    return render_to_response('500.html', msg)
            else:
                msg = {'status': '密码输入不一致！'}
                return render_to_response('500.html', msg)
        else:
            msg = {'status': '用户名密码或邮箱不能为空！'}
            return render_to_response('500.html', msg)
    return render_to_response('account/register.html', msg)


def active(request, *args, **kwargs):
    token = kwargs['token']
    # 拿参数对应的缓存数据
    email = cache.get(token)
    # print(res)
    if email:
        # 通过邮箱找到对应用户
        # 给用户的状态字段做更新，从未激活变成激活状态
        username = userInfo.objects.filter(email=email).values('username')
        userInfo.objects.filter(email=email).update(is_active=1)
        msg = '恭喜你,' + email + '激活成功!'
    else:
        msg = '该链接已经失效！'
    return render_to_response('account/active.html', {'msg': msg, })


def forget_pass_form_1(request, *args, **kwargs):
    status = ''
    return render_to_response('account/forget_pass_1.html', {'status': status})


def forget_pass_form_2(request, *args, **kwargs):
    username = request.POST.get('username', None)
    if username:

        is_exist = bool(userInfo.objects.filter(username=username))
        # print(username, is_exist, type(username), type(is_exist))

        # 2023/12/12 增加是否被禁用判断
        is_active = userInfo.objects.filter(username=username).values('is_active')[0]['is_active']
        print(is_active, type(is_active))

        if not is_exist:
            status = '该用户不存在！'
            msg = {'status': status}
            # return render_to_response('forget_pass_2-error.html', msg)
            # return redirect('/cmdb/login/forget_pass/step/1/')
            return render_to_response('account/forget_pass_1.html', msg)

        elif not is_active:
            status = '该用户已经禁用！'
            msg = {'status': status}
            return render_to_response('account/forget_pass_1.html', msg)
        else:
            email = userInfo.objects.filter(username=username).values('email')
            status = ''
            msg = {'email': email, 'username': username, 'status': status}
            # return render_to_response('forget_pass_2.html', msg)
            return render_to_response('account/forget_pass_2.html', msg)
    else:
        status = '用户名不能为空！'
        msg = {'status': status}
        # return render_to_response('forget_pass_2-error.html', msg)
        # return redirect('/cmdb/login/forget_pass/step/1/')
        return render_to_response('account/forget_pass_1.html', msg)


# @xframe_options_sameorigin
def forget_pass_send(request, *args, **kwargs):
    if request.method == 'POST':
        # 去除换行和空格
        email = request.POST.get('email').strip()
        # print(email,type(email))
        username = request.POST.get('username')
        verify_code = token_helper.get_random_code()
        tasks.account_send_email_code.delay(email, verify_code)
        request.session['verify_code'] = verify_code
        status = '邮件已发送！'
        # msg = {'status':status,}
        msg = {'status': status, 'email': email, 'username': username}
        # return redirect('/cmdb/login/forget_pass/send/verify_code=' + verify_code + '&email=' + email)
        return render_to_response('account/forget_pass_2-send.html', msg)

    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            verify_code = request.session.get('verify_code')
            email = cache.get(verify_code)
            if code == verify_code:
                return redirect('/cmdb/login/forget_pass/change/?verify_code=' + verify_code + '&email=' + email)
            else:
                status = '验证码错误！'
        else:
            status = '请输入验证码！'
        msg = {'status': status, }
        return render_to_response('account/forget_pass_2-send.html', msg)


def forget_pass_change(request, *args, **kwargs):
    if request.method == 'GET':
        verify_code = request.GET.get('verify_code')
        email = request.GET.get('email')
        request.session['email'] = email
        status = ''
        msg = {'status': status}
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.session.get('email')
        if password1 == password2:
            # password = encrypt_helper.md5_encrypt(password2)
            status = '修改成功！'
            msg = {'status': status}
            # userInfo.objects.filter(email=email).update(password=password,update_time=timezone.now())
            queryset = get_object_or_404(userInfo, email=email)
            queryset.set_password(password2)  # 设置密码
            queryset.save()  # 保存
    return render_to_response('account/forget_pass_3.html', msg)


@custom_login_required
def search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/table/user/search_result/keyword=' + keyword + '&page=' + page)
        # return redirect(reverse("account.search_result", kwargs={"keyword": keyword, "page": page}))
    else:
        return redirect('/cmdb/index/table/user/list/')
        # return redirect(reverse("account.user", kwargs={"page": page}))


@custom_login_required
def search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    userinfo = userInfo.objects.filter(username__icontains=keyword) | userInfo.objects.filter(
        email__icontains=keyword)
    count = userinfo.count()
    userDict = request.session.get('is_login', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    userinfo = userinfo[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_user_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'userinfo': userinfo, 'login_user': userDict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string, }
    # return render_to_response('user_search.html',msg)
    return render_to_response('account/user.html', msg)


@custom_login_required
@custom_permission_required('auth.add_group')
def usergroupForm_add(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    # usergroup = userGroup.objects.all()
    usergroup = Group.objects.all()
    userDict = request.session.get('is_login', None)
    perm = Permission.objects.all()
    msg = {'userinfo': userinfo, 'usergroup': usergroup,
           'login_user': userDict['user'], 'status': '', 'perm': perm, }
    return render_to_response('account/usergroup_add.html', msg)


@custom_login_required
@custom_permission_required('auth.add_group')
def usergroupAdd(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        usergroup = request.POST.get('usergroup', None)
        perm = request.POST.getlist('perm', None)
        # is_exist = userGroup.objects.filter(name=usergroup)
        is_exist = Group.objects.filter(name=usergroup)
        # print(is_exist)
        if not (is_exist):
            is_empty = all([usergroup, perm])
            if is_empty:
                # userGroup.objects.create(name=usergroup,)
                queryset = Group.objects.create(name=usergroup, )
                queryset.permissions.set(perm)  # set:批量增加，add：增加，remove：删除，clear：清除所有
                msg = {'userinfo': userinfo,
                       'login_user': userDict['user'], 'status': '添加组/角色成功', }
                return redirect('/cmdb/index/table/usergroup/list/')
            else:
                msg = {'userinfo': userinfo,
                       'login_user': userDict['user'], 'status': '组/角色名称或者权限不能为空', }
                return render_to_response('500.html', msg)
        else:
            msg = {'userinfo': userinfo, 'usergroup': usergroup,
                   'login_user': userDict['user'], 'status': '该组/角色已存在！', }
            return render_to_response('500.html', msg)


@custom_login_required
@custom_permission_required('auth.change_group')
def usergroupForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    usergroup = Group.objects.filter(id=id)
    # usergroup = userGroup.objects.filter(id=id)
    usergroup_obj = get_object_or_404(Group, pk=id)
    userDict = request.session.get('is_login', None)
    perm = Permission.objects.all().exclude(group=usergroup_obj)
    perm_selected = Permission.objects.filter(group=usergroup_obj)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'usergroup': usergroup,
           'perm': perm, 'perm_selected': perm_selected, }
    # print(msg)
    return render_to_response('account/usergroup_update.html', msg)


@custom_login_required
@custom_permission_required('auth.view_group')
def usergroupDetail(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    usergroup = Group.objects.filter(id=id)
    # usergroup = userGroup.objects.filter(id=id)
    usergroup_obj = get_object_or_404(Group, pk=id)
    usergroup_name = usergroup_obj.name
    userDict = request.session.get('is_login', None)
    perm = Permission.objects.all().exclude(group=usergroup_obj)
    perm_selected = Permission.objects.filter(group=usergroup_obj)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'usergroup': usergroup,
           'usergroup_name': usergroup_name, 'perm': perm, 'perm_selected': perm_selected, }
    # print(msg)
    return render_to_response('account/usergroup_detail.html', msg)


@custom_login_required
@custom_permission_required('auth.change_group')
def usergroupUpdate(request, *args, **kwargs):
    id = kwargs['id']
    usergroup = request.POST.get('usergroup', None)
    perm = request.POST.getlist('perm', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    # userGroup.objects.filter(id=id).update(name=usergroup,update_time=update_time)
    is_empty = all([usergroup, perm])
    if is_empty:
        Group.objects.filter(id=id).update(name=usergroup)
        queryset = get_object_or_404(Group, pk=id)
        queryset.permissions.set(perm)
        return redirect('/cmdb/index/table/usergroup/list/')
    else:
        msg = {
            'login_user': userDict['user'], 'status': '组/角色名称或者权限不能为空', }
        return render_to_response('500.html', msg)


@custom_login_required
@custom_permission_required('auth.view_group')
def usergroup(request, *args, **kwargs):
    # usergroup=userGroup.objects.all()
    usergroup = Group.objects.all()
    count = Group.objects.all().count()
    userDict = request.session.get('is_login', None)
    msg = {'usergroup': usergroup, 'login_user': userDict['user'], 'count': count}
    return render_to_response('account/usergroup.html', msg)


@custom_login_required
@custom_permission_required('auth.delete_group')
def usergroupDel(request, *args, **kwargs):
    id = request.POST.get('id')
    # userGroup.objects.filter(id=id).delete()
    Group.objects.filter(id=id).delete()
    # print('delete',id)
    msg = {'code': 1, 'result': '删除用户组id:' + id, }
    return render_to_response('account/usergroup.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_userinfo')
def userForm_add(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    # usergroup = userGroup.objects.all()
    usergroup = Group.objects.all()
    perm = Permission.objects.all()
    userDict = request.session.get('is_login', None)
    user_obj = get_object_or_404(userInfo, username=userDict['user'])
    # print(request.user,request.user.has_perm('myapp.add_userinfo'))
    # print(user_obj, user_obj.has_perm('myapp.add_userinfo'))
    msg = {'userinfo': userinfo, 'usergroup': usergroup,
           'login_user': userDict['user'], 'status': '', 'perm': perm, }
    return render_to_response('account/user_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_userinfo')
def userAdd(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = userGroup.objects.all()
    usergroup = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        is_exist = userInfo.objects.filter(username=username) | userInfo.objects.filter(email=email)
        # is_exist = userInfo.objects.filter(username=username)
        # print(is_exist)
        if not (is_exist):
            password_origin = request.POST.get('password', None)
            # password = encrypt_helper.md5_encrypt(password_origin)
            # print(password,type(password))
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            is_superuser = request.POST.get('is_superuser', None)
            is_staff = request.POST.get('is_staff', None)
            group = request.POST.getlist('group', None)
            perm = request.POST.getlist('perm', None)
            workflow_order = request.POST.get('workflow_order', None)
            is_active = request.POST.get('is_active', None)
            memo = request.POST.get('memo', None)
            # is_empty = all([username,password,email,usertype_select,])
            is_empty = all([username, password_origin, email, ])
            if is_empty:
                # queryset=userInfo.objects.create(username=username, password=password,
                #     email=email,usertype=usertype_select,memo=memo,workflow_order=workflow_order,is_active=is_active,)
                # queryset.group.set(group)
                queryset = userInfo.objects.create(username=username, email=email, first_name=first_name,
                                                   last_name=last_name,
                                                   is_superuser=is_superuser, is_staff=is_staff,
                                                   workflow_order=workflow_order, is_active=is_active, memo=memo, )
                queryset.groups.set(group)  # 添加到组/角色
                queryset.user_permissions.set(perm)  # set:批量增加，add：增加，remove：删除，clear：清除所有
                queryset.set_password(password_origin)  # 设置密码
                queryset.save()  # 保存
                '''
                queryset.has_perm(perm)  #是否具有权限
                queryset.get_all_permission()  #获取所有权限
                queryset.get_group_permission()  #获取用户所属组/角色的权限
                '''
                msg = {'userinfo': userinfo,
                       'login_user': userDict['user'], 'status': '添加用户成功', }
                return redirect('/cmdb/index/table/user/list/')
            else:
                msg = {'userinfo': userinfo,
                       'login_user': userDict['user'], 'status': '带 * 选项不能为空', }
                return render_to_response('500.html', msg)
        else:
            if userInfo.objects.filter(username=username):
                status = '该用户名已存在！'
            else:
                status = '该邮箱已存在！'
            msg = {'userinfo': userinfo, 'usergroup': usergroup,
                   'login_user': userDict['user'], 'status': status}
            return render_to_response('500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_userinfo')
def userForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    userid = kwargs['userid']
    userinfo = userInfo.objects.filter(id=userid)
    userinfo_obj = get_object_or_404(userInfo, id=userid)
    # usertype_selected = userType.objects.filter(userinfo__id=userid)
    # 返回的QuerySet为对象字典集，'usertype_selected': <QuerySet [<userType: userType object (1)>]>,
    # usertype_selected = userinfo.values('usertype')
    # 返回的QuerySet为元素字典集，'usertype_selected': <QuerySet [{'usertype': 1}]>,
    # foo = usertype_selected.first().userinfo_set.values('username')
    # 根据对象反向查询，返回的QuerySet为元素字典集，<QuerySet [{'username': 'admin'}, {'username': 'user1'}]>
    # foo = usertype_selected.first().userinfo_set.all()
    # 根据对象反向查询，返回的QuerySet为对象字典集，<QuerySet [<userInfo: userInfo object (1)>, <userInfo: userInfo object (2)>]>
    # eg：从用户类型反向查找用户
    # print(foo,)
    # usertype = userType.objects.all().exclude(userinfo__id=userid)
    # group_selected = userGroup.objects.filter(userinfo__id=userid)
    # group = userGroup.objects.all().exclude(userinfo__id=userid)
    group_selected = Group.objects.filter(user=userinfo_obj)
    group = Group.objects.all().exclude(user=userinfo_obj)
    userDict = request.session.get('is_login', None)
    perm = Permission.objects.all().exclude(user=userinfo_obj)
    perm_selected = Permission.objects.filter(user=userinfo_obj)

    # msg = {'userid':userid,'userinfo':userinfo,'login_user':userDict['user'],'status':'操作成功','usertype':usertype,
    #       'usertype_selected':usertype_selected,'group':group,'group_selected':group_selected,}
    msg = {'userid': userid, 'userinfo': userinfo, 'login_user': userDict['user'], 'status': '操作成功',
           'group': group, 'group_selected': group_selected, 'perm': perm, 'perm_selected': perm_selected, }
    # print(msg,)
    return render_to_response('account/user_update.html', msg)
    # return HttpResponse(json.dumps(msg))


@custom_login_required
def userForm_change_password(request, *args, **kwargs):
    username = kwargs['username']
    userinfo = userInfo.objects.filter(username=username)
    userDict = request.session.get('is_login', None)
    msg = {'username': username, 'userinfo': userinfo, 'login_user': userDict['user'], 'status': '操作成功', }
    # print(msg, )
    return render_to_response('account/settings.html', msg)


@custom_login_required
def userForm_get_profile(request, *args, **kwargs):
    username = kwargs['username']
    userinfo = userInfo.objects.filter(username=username)
    # usertype_selected = userType.objects.filter(userinfo__username=username)
    # usertype = userType.objects.all().exclude(userinfo__username=username)
    # group_selected = userGroup.objects.filter(userinfo__username=username)
    # group = userGroup.objects.all().exclude(userinfo__username=username)
    userDict = request.session.get('is_login', None)
    user_obj = get_object_or_404(userinfo, username=userDict['user'])
    group_selected = Group.objects.filter(user=user_obj)
    '''
    if not group_selected:
        group_selected = None
    '''
    group = Group.objects.all().exclude(user=user_obj)
    is_superuser = user_obj.is_superuser
    if is_superuser:
        perm_selected = Permission.objects.all()
    else:
        perm_selected = Permission.objects.filter(user=user_obj)
    perm = Permission.objects.all().exclude(user=user_obj)
    # msg = {'username':username,'userinfo':userinfo,'login_user':userDict['user'],'status':'操作成功','usertype':usertype,
    #       'usertype_selected':usertype_selected,'group':group,'group_selected':group_selected,}
    msg = {'username': username, 'userinfo': userinfo, 'login_user': userDict['user'], 'status': '操作成功',
           'group_selected': group_selected, 'group': group, 'perm_selected': perm_selected, 'perm': perm, }
    # print(msg, )
    return render_to_response('account/profile.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_userinfo')
def userUpdate(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    userDict = request.session.get('is_login', None)
    userid = kwargs['userid']
    username = request.POST.get('username', None)
    # password_origin = request.POST.get('password', None)
    # print(password_origin)
    # password = encrypt_helper.md5_encrypt(password_origin)
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    is_superuser = request.POST.get('is_superuser', None)
    is_staff = request.POST.get('is_staff', None)
    email = request.POST.get('email', None)
    usertype = request.POST.get('usertype', None)
    group = request.POST.getlist('group', None)
    perm = request.POST.getlist('perm', None)
    workflow_order = request.POST.get('workflow_order', None)
    is_active = request.POST.get('is_active', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    # print(username, email, usertype, group, memo, perm, )
    userDict = request.session.get('is_login', None)
    # userInfo.objects.filter(id=userid).update(username=username,workflow_order=workflow_order,
    #         email=email,usertype=usertype,memo=memo,update_time=update_time,is_active=is_active,)
    is_empty = all([username, email, ])
    if is_empty:
        userInfo.objects.filter(id=userid).update(username=username, workflow_order=workflow_order,
                                                  email=email, memo=memo, is_active=is_active, first_name=first_name,
                                                  last_name=last_name, is_superuser=is_superuser, is_staff=is_staff)
        queryset = get_object_or_404(userInfo, id=userid)
        # queryset.group.set(group)
        queryset.groups.set(group)  # 设置组/角色
        queryset.user_permissions.set(perm)  # 设置权限
        # 取消密码修改，通过用户个人账户修改或者管理员重置密码方式修改
        # queryset.set_password(password_origin)  # 设置密码
        queryset.save()  # 保存
        return redirect('/cmdb/index/table/user/list/')
        # return render_to_response('user.html',msg)
        # return HttpResponse(json.dumps(msg))
    else:
        msg = {'userinfo': userinfo,
               'login_user': userDict['user'], 'status': '带 * 选项不能为空', }
        return render_to_response('500.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_userinfo')
def userDetail(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['userid']
    userinfo = userInfo.objects.filter(id=id)
    # usergroup = userGroup.objects.filter(id=id)
    userinfo_obj = get_object_or_404(userInfo, pk=id)
    username = userinfo_obj.username
    first_name = userinfo_obj.first_name
    last_name = userinfo_obj.last_name
    email = userinfo_obj.email
    is_staff = userinfo_obj.is_staff
    is_active = userinfo_obj.is_active
    date_joined = userinfo_obj.date_joined
    workflow_order = userinfo_obj.workflow_order
    password = userinfo_obj.password
    last_login = userinfo_obj.last_login
    is_superuser = userinfo_obj.is_superuser
    memo = userinfo_obj.memo
    group_selected = Group.objects.filter(user=userinfo_obj)
    group = Group.objects.all().exclude(user=userinfo_obj)
    userDict = request.session.get('is_login', None)
    perm = Permission.objects.all().exclude(user=userinfo_obj)
    if is_superuser:
        perm_selected = Permission.objects.all()
    else:
        perm_selected = Permission.objects.filter(user=userinfo_obj)

    msg = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'is_staff': is_staff,
           'is_active': is_active,
           'date_joined': date_joined, 'workflow_order': workflow_order, 'password': password, 'last_login': last_login,
           'is_superuser': is_superuser,
           'memo': memo, 'login_user': userDict['user'], 'status': '操作成功', 'usergroup': usergroup,
           'perm': perm, 'perm_selected': perm_selected, 'userinfo': userinfo, 'group_selected': group_selected, }

    # print(msg)
    return render_to_response('account/user_detail.html', msg)


@custom_login_required
def user_change_password(request, *args, **kwargs):
    username = kwargs['username']
    password_origin = request.POST.get('password_origin', None)
    password_new1 = request.POST.get('password_new1', None)
    password_new2 = request.POST.get('password_new2', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    # is_valid = userInfo.objects.filter(username=username,password=encrypt_helper.md5_encrypt(password_origin)).count()
    # if is_valid != 1:
    # 校验原密码是否输入和数据库一致
    is_valid = userInfo.objects.get(username=username).check_password(password_origin)
    if not is_valid:
        msg = {'status': '原密码输入错误，请重新输入', 'login_user': userDict['user'], }
        # return render_to_response('500.html', msg)
    elif not password_new1:
        msg = {'status': '密码不能为空，请重新输入', 'login_user': userDict['user'], }
    elif password_new1 != password_new2:
        msg = {'status': '两次密码输入不一致，请重新输入', 'login_user': userDict['user'], }
        # return render_to_response('500.html',msg)
    else:
        msg = {'status': '修改成功', 'login_user': userDict['user'], }
        # userInfo.objects.filter(username=username).update(password=encrypt_helper.md5_encrypt(password_new2),update_time=update_time,)
        user = get_object_or_404(userInfo, username=username)
        user.set_password(password_new2)
        user.save()
        # return redirect('/cmdb/index/table/user/')
    # return render_to_response('account/settings.html', msg)
    return HttpResponse(json.dumps(msg))


@custom_login_required
@custom_permission_required('myapp.change_userinfo')
def resetPwd(request, *args, **kwargs):
    userid = request.POST.get('userid', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    # userInfo.objects.filter(id=userid).update(password=encrypt_helper.md5_encrypt('123456'),update_time=update_time,)
    user = get_object_or_404(userInfo, pk=userid)
    res = user.set_password('password')
    ret = user.save()
    # print(ret, type(ret), res)
    msg = {'login_user': userDict['user'], 'ret': ret, 'res': res}
    # return render_to_response('account/user.html', msg)
    return HttpResponse(json.dumps(msg))


@custom_login_required
@custom_permission_required('myapp.view_userinfo')
def user(request, *args, **kwargs):
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    count = userInfo.objects.all().count()
    pageinfo = page_helper.pageinfo(page, count, perItem)
    userinfo = userInfo.objects.all()[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_user_list(request, page, pageinfo.pageCount)
    # usertype = userType.objects.all()
    userDict = request.session.get('is_login', None)
    # if not userDict:
    #    return redirect('/cmdb/login/')
    msg = {'userinfo': userinfo, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': userDict['user'], }
    response = render_to_response('account/user.html', msg, )
    # response.set_cookie('k1','v1')
    # print(request.COOKIES)
    # print(request.COOKIES.get('page_num'))
    # print(args,kwargs)
    return response


@custom_login_required
@custom_permission_required('myapp.delete_userinfo')
def userDel(request, *args, **kwargs):
    id = request.POST.get('userid')
    username = userInfo.objects.filter(id=id).values('username')[0]['username']
    userInfo.objects.filter(id=id).delete()
    # print('delete', id)
    msg = {'code': 1, 'status': '删除用户' + username + '成功', }
    return render_to_response('account/user.html', msg)


@custom_login_required
@custom_permission_required('auth.view_permission')
def permission(request, *args, **kwargs):
    page = common.try_int(kwargs['page'], 1)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    count = Permission.objects.all().count()
    pageinfo = page_helper.pageinfo(page, count, perItem)
    perm = Permission.objects.all()[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_perm_list(request, page, pageinfo.pageCount)
    # usertype = userType.objects.all()
    userDict = request.session.get('is_login', None)
    # print(perm)
    msg = {'perm': perm, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': userDict['user'], }
    return render_to_response('account/permission.html', msg)
