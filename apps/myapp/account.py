#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.db.models import Q
from django.http import JsonResponse
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

########################################################################################################################
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
    usergroup = Group.objects.all()
    usergroup_count = usergroup.count()
    user_count = userInfo.objects.all().count()
    deploy_count = deploy_app.objects.all().count()
    deploy_list_count = deploy_list_detail.objects.all().count()
    wf_count = wf_info.objects.all().count()
    asset_count = Asset.objects.all().count()
    # prometheus_alert_count = prometheus.prometheus_alert_count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'userinfo': userinfo, 'login_user': user_dict['user'], 'usergroup_count': usergroup_count,
           'user_count': user_count, 'deploy_count': deploy_count, 'wf_count': wf_count,
           # 'zabbix_alert_count':zabbix_alert_count,'prometheus_alert_count':prometheus_alert_count,}
           'deploy_list_count': deploy_list_count,
           'wf_count_pending': wf_dict['wf_count_pending'], 'asset_count': asset_count}
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
        is_auth = authenticate(username=username, password=password_origin)
        remember = request.POST.get('remember', None)
        is_empty = all([username, password_origin])
        # print(username, password_origin,remember,is_empty,user,type(user))
        if is_empty:
            if is_auth:
                request.session['is_login'] = {'user': username, 'pass': password, }
                # 2024/5/6 wf待办信息写入session
                wf_count_pending = wf_info.objects.filter(next_assignee=username).filter(
                    flow_id__gte=0).filter(
                    ~Q(status='已完成')).count()
                # print(wf_count_pending)
                request.session['wf'] = {'wf_count_pending': wf_count_pending, }
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
                    return render_to_response('500.html', msg, status=500)
            else:
                msg = {'status': '密码输入不一致！'}
                return render_to_response('500.html', msg, status=500)
        else:
            msg = {'status': '用户名密码或邮箱不能为空！'}
            return render_to_response('500.html', msg, status=500)
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


# @xframe_options_sameorigin
def forget_pass_send(request, *args, **kwargs):
    if request.method == 'POST':
        # 去除换行和空格
        email = request.POST.get('email').strip()
        print('email:', email, type(email))
        # 判断是否为空
        if email:
            is_exist = userInfo.objects.filter(email=email)
            print(is_exist)
            is_active = userInfo.objects.filter(email=email).values('is_active')[0]['is_active']
            print(is_active, type(is_active))
            # 判断用户邮箱是否存在
            if not is_exist:
                result = '系统中该邮箱地址不存在！'
                msg = {'result': result, }
                return JsonResponse(msg, status=500)
            # 判断用户状态
            elif not is_active:
                result = '该用户已经禁用！'
                msg = {'result': result}
                return JsonResponse(msg, status=500)
            else:
                verify_code = token_helper.get_random_code()
                tasks.account_send_email_code.delay(email, verify_code)
                cache.set('verify_code', verify_code)
                cache.set('email', email)
                result = '邮件已发送！'
                msg = {'result': result, }
                return JsonResponse(msg, )
        else:
            result = '请先输入邮箱地址！'
            msg = {'result': result, }
            return JsonResponse(msg, status=500)
    else:
        result = '请使用post方法提交！'
        msg = {'result': result, }
        return JsonResponse(msg, status=405)


def forget_pass_change(request, *args, **kwargs):
    if request.method == 'POST':
        verify_code = request.POST.get('verify_code', None)
        email = request.POST.get('email', None)
        password = request.POST.get('pwd', None)
        password_confirm = request.POST.get('pwd_confirm')
        # verify_code_confirm = cache.get('verify_code')
        required_field = [email, verify_code, password, password_confirm]
        print(required_field)
        if all(required_field):
            # 校验验证码所属邮箱是否对应
            print(cache.get(verify_code))
            if email == cache.get(verify_code):
                if password == password_confirm:
                    # password = encrypt_helper.md5_encrypt(password2)
                    # userInfo.objects.filter(email=email).update(password=password,update_time=timezone.now())
                    queryset = get_object_or_404(userInfo, email=email)
                    queryset.set_password(password_confirm)  # 设置密码
                    queryset.save()  # 保存
                    status = '密码设置成功！'
                    msg = {'status': status}
                    return render_to_response('account/login.html', msg)
                else:
                    status = '两次密码输入不一致！errcode: 3'
            else:
                status = '验证码错误！errcode: 2'
        else:
            status = "字段不能为空：['email', 'verify_code', 'password', 'password_confirm'],errcode: 1"
        msg = {'status': status, }
        return render_to_response('500.html', msg, status=500)
    else:
        status = '请使用post方法提交！'
        msg = {'status': status, }
        return render_to_response('500.html', msg, status=405)


@custom_login_required
@custom_permission_required('myapp.view_userinfo')
def user_search(request, *args, **kwargs):
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
@custom_permission_required('myapp.view_userinfo')
def user_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    userinfo = userInfo.objects.filter(username__icontains=keyword) | userInfo.objects.filter(
        email__icontains=keyword)
    count = userinfo.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, perItem, keyword)
    userinfo = userinfo[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_user_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'userinfo': userinfo, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('account/user.html', msg)


@custom_login_required
@custom_permission_required('auth.add_group')
def usergroup_form_add(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    # usergroup = userGroup.objects.all()
    qs_usergroup = Group.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    perm = Permission.objects.all()
    msg = {'userinfo': userinfo, 'usergroup': qs_usergroup,
           'login_user': user_dict['user'], 'status': '', 'perm': perm,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('account/usergroup_add.html', msg)


@custom_login_required
@custom_permission_required('auth.add_group')
def usergroup_add(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        usergroup_name = request.POST.get('usergroup', None)
        perm_list = request.POST.getlist('perm', None)
        is_exist = Group.objects.filter(name=usergroup_name)
        # print(is_exist)
        if not is_exist:
            is_empty = all([usergroup_name, ])
            if is_empty:
                queryset = Group.objects.create(name=usergroup_name, )
                # 判断提交的标签是否包含空标签：当不含空标签，
                if '' not in perm_list:
                    # 设置标签
                    queryset.permissions.set(perm_list)
                    print('1')
                # 判断提交的标签是否包含空标签：当含有空标签，
                else:
                    # 清除空元素，设置标签
                    perm_list.remove('')
                    queryset.permissions.set(perm_list)
                    print('2')
                # set:批量增加，add：增加，remove：删除，clear：清除所有
                # queryset.permissions.set(perm_list)
                msg = {'userinfo': userinfo,
                       'login_user': user_dict['user'], 'status': '添加组/角色成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/table/usergroup/list/')
            else:
                msg = {'userinfo': userinfo,
                       'login_user': user_dict['user'], 'status': '组/角色名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return render_to_response('500.html', msg, status=500)
        else:
            msg = {'userinfo': userinfo,
                   'login_user': user_dict['user'], 'status': '该组/角色已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=500)


@custom_login_required
@custom_permission_required('auth.change_group')
def usergroup_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs_usergroup = Group.objects.filter(id=form_id)
    # usergroup = userGroup.objects.filter(id=id)
    usergroup_obj = get_object_or_404(Group, pk=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    perm = Permission.objects.all().exclude(group=usergroup_obj)
    perm_selected = Permission.objects.filter(group=usergroup_obj)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'usergroup': qs_usergroup,
           'perm': perm, 'perm_selected': perm_selected, 'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('account/usergroup_update.html', msg)


@custom_login_required
@custom_permission_required('auth.view_group')
def usergroup_detail(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs_usergroup = Group.objects.filter(id=form_id)
    # usergroup = userGroup.objects.filter(id=id)
    usergroup_obj = get_object_or_404(Group, pk=form_id)
    usergroup_name = usergroup_obj.name
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    perm = Permission.objects.all().exclude(group=usergroup_obj)
    perm_selected = Permission.objects.filter(group=usergroup_obj)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'usergroup': qs_usergroup,
           'usergroup_name': usergroup_name, 'perm': perm, 'perm_selected': perm_selected,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('account/usergroup_detail.html', msg)


@custom_login_required
@custom_permission_required('auth.change_group')
def usergroup_update(request, *args, **kwargs):
    form_id = kwargs['id']
    # print(form_id)
    usergroup_name = request.POST.get('usergroup', None)
    perm_list = request.POST.getlist('perm', None)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    is_empty = all([usergroup_name, ])
    if is_empty:
        queryset = get_object_or_404(Group, pk=form_id)
        qs = Group.objects.filter(id=form_id)
        qs.update(name=usergroup_name)
        # 判断提交的标签是否包含空标签：当不含空标签，
        if '' not in perm_list:
            # 设置标签
            queryset.permissions.set(perm_list)
            print('1')
        # 判断提交的标签是否包含空标签：当含有空标签，
        else:
            # 清除空元素，设置标签
            perm_list.remove('')
            queryset.permissions.set(perm_list)
            print('2')
        return redirect('/cmdb/index/table/usergroup/list/')
    else:
        msg = {
            'login_user': user_dict['user'], 'status': '组/角色名称或者权限不能为空',
            'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=500)


@custom_login_required
@custom_permission_required('auth.view_group')
def usergroup(request, *args, **kwargs):
    # usergroup=userGroup.objects.all()
    # 默认降序排列，很特殊
    qs_usergroup = Group.objects.all().order_by('id')
    count = Group.objects.all().count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'usergroup': qs_usergroup, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('account/usergroup.html', msg)


@custom_login_required
# @custom_permission_required('auth.delete_group')
def usergroup_del(request, *args, **kwargs):
    form_id = request.POST.get('id')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.delete_userinfo'):
        # userGroup.objects.filter(id=id).delete()
        Group.objects.filter(id=form_id).delete()
        # print('delete',id)
        msg = {'code': '1', 'result': '删除用户组id:' + form_id, }
        return render_to_response('account/usergroup.html', msg)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


@custom_login_required
# @custom_permission_required('myapp.delete_group')
def usergroup_del_all(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.delete_userinfo'):
        Group.objects.filter(id__in=array_id).delete()
        print('delete', array_id)
        msg = {'code': '0', 'status': '删除用户组成功,id列表：' + json.dumps(array_id)}
        print(msg)
        return render_to_response('account/usergroup.html', msg)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


@custom_login_required
@custom_permission_required('myapp.add_userinfo')
def user_form_add(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    # usergroup = userGroup.objects.all()
    qs_usergroup = Group.objects.all()
    perm = Permission.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    # print(request.user,request.user.has_perm('myapp.add_userinfo'))
    # print(user_obj, user_obj.has_perm('myapp.add_userinfo'))
    msg = {'userinfo': userinfo, 'usergroup': qs_usergroup,
           'login_user': user_dict['user'], 'status': '', 'perm': perm,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('account/user_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_userinfo')
def user_add(request, *args, **kwargs):
    qs_userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # usergroup = userGroup.objects.all()
    qs_usergroup = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password_origin = request.POST.get('password', None)
        # password = encrypt_helper.md5_encrypt(password_origin)
        # print(password,type(password))
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        is_superuser = request.POST.get('is_superuser', None)
        is_staff = request.POST.get('is_staff', None)
        group_list = request.POST.getlist('group', None)
        perm_list = request.POST.getlist('perm', None)
        workflow_order = request.POST.get('workflow_order', None)
        is_active = request.POST.get('is_active', None)
        memo = request.POST.get('memo', None)
        required_field = [username, password_origin, email, ]
        is_empty = all(required_field)
        if is_empty:
            is_exist = userInfo.objects.filter(Q(username=username) | Q(email=email))
            print(is_exist)
            if not is_exist:
                # queryset=userInfo.objects.create(username=username, password=password,
                #     email=email,usertype=usertype_select,memo=memo,workflow_order=workflow_order,is_active=is_active,)
                # queryset.group.set(group)
                queryset = userInfo.objects.create(username=username, email=email, first_name=first_name,
                                                   last_name=last_name,
                                                   is_superuser=is_superuser, is_staff=is_staff,
                                                   workflow_order=workflow_order, is_active=is_active, memo=memo, )
                '''
                queryset.groups.set(group_list)  # 添加到组/角色
                queryset.user_permissions.set(perm_list)  # set:批量增加，add：增加，remove：删除，clear：清除所有
                '''
                # 判断提交的标签是否包含空标签：当不含空标签，
                if '' not in group_list:
                    # 设置标签
                    queryset.groups.set(group_list)
                    print('1')
                # 判断提交的标签是否包含空标签：当含有空标签，
                else:
                    # 清除空元素，设置标签
                    group_list.remove('')
                    queryset.groups.set(group_list)
                    print('2')
                # 判断提交的标签是否包含空标签：当不含空标签，
                if '' not in perm_list:
                    # 设置标签
                    queryset.user_permissions.set(perm_list)
                    print('3')
                # 判断提交的标签是否包含空标签：当含有空标签，
                else:
                    # 清除空元素，设置标签
                    perm_list.remove('')
                    queryset.user_permissions.set(perm_list)
                    print('4')
                queryset.set_password(password_origin)  # 设置密码
                queryset.save()  # 保存
                '''
                queryset.has_perm(perm)  #是否具有权限
                queryset.get_all_permission()  #获取所有权限
                queryset.get_group_permission()  #获取用户所属组/角色的权限
                '''
                msg = {'userinfo': qs_userinfo,
                       'login_user': user_dict['user'], 'status': '添加用户成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/table/user/list/')
            else:
                if userInfo.objects.filter(username=username):
                    status = '该用户名已存在！'
                if userInfo.objects.filter(email=email):
                    status = '该邮箱已存在！'
                msg = {'userinfo': qs_userinfo, 'usergroup': qs_usergroup,
                       'login_user': user_dict['user'], 'status': status,
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return render_to_response('500.html', msg, status=500)
        else:
            msg = {'userinfo': qs_userinfo,
                   'login_user': user_dict['user'], 'status': '[username, password, email, ]不能为空',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=500)
    else:
        msg = {
            'login_user': user_dict['user'], 'status': '使用POST方法',
            'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=405)


@custom_login_required
@custom_permission_required('myapp.change_userinfo')
def user_form_update(request, *args, **kwargs):
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
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    perm = Permission.objects.all().exclude(user=userinfo_obj)
    perm_selected = Permission.objects.filter(user=userinfo_obj)

    # msg = {'userid':userid,'userinfo':userinfo,'login_user':userDict['user'],'status':'操作成功','usertype':usertype,
    #       'usertype_selected':usertype_selected,'group':group,'group_selected':group_selected,}
    msg = {'userid': userid, 'userinfo': userinfo, 'login_user': user_dict['user'], 'status': '操作成功',
           'group': group, 'group_selected': group_selected, 'perm': perm, 'perm_selected': perm_selected,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg,)
    return render_to_response('account/user_update.html', msg)
    # return HttpResponse(json.dumps(msg))


@custom_login_required
def user_form_change_password(request, *args, **kwargs):
    username = kwargs['username']
    userinfo = userInfo.objects.filter(username=username)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'username': username, 'userinfo': userinfo, 'login_user': user_dict['user'], 'status': '操作成功',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg, )
    return render_to_response('account/settings.html', msg)


@custom_login_required
def user_form_get_profile(request, *args, **kwargs):
    username = kwargs['username']
    userinfo = userInfo.objects.filter(username=username)
    # usertype_selected = userType.objects.filter(userinfo__username=username)
    # usertype = userType.objects.all().exclude(userinfo__username=username)
    # group_selected = userGroup.objects.filter(userinfo__username=username)
    # group = userGroup.objects.all().exclude(userinfo__username=username)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    user_obj = get_object_or_404(userinfo, username=user_dict['user'])
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
    msg = {'username': username, 'userinfo': userinfo, 'login_user': user_dict['user'], 'status': '操作成功',
           'group_selected': group_selected, 'group': group, 'perm_selected': perm_selected, 'perm': perm,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg, )
    return render_to_response('account/profile.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_userinfo')
def user_update(request, *args, **kwargs):
    userinfo = userInfo.objects.all()
    # usertype = userType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
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
    group_list = request.POST.getlist('group', None)
    perm_list = request.POST.getlist('perm', None)
    workflow_order = request.POST.get('workflow_order', None)
    is_active = request.POST.get('is_active', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    # print(username, email, usertype, group, memo, perm, )
    # user_dict = request.session.get('is_login', None)
    # userInfo.objects.filter(id=userid).update(username=username,workflow_order=workflow_order,
    #         email=email,usertype=usertype,memo=memo,update_time=update_time,is_active=is_active,)
    is_empty = all([username, email, ])
    if is_empty:
        userInfo.objects.filter(id=userid).update(username=username, workflow_order=workflow_order,
                                                  email=email, memo=memo, is_active=is_active, first_name=first_name,
                                                  last_name=last_name, is_superuser=is_superuser, is_staff=is_staff)
        queryset = get_object_or_404(userInfo, id=userid)
        '''
        # queryset.group.set(group)
        queryset.groups.set(group)  # 设置组/角色
        queryset.user_permissions.set(perm)  # 设置权限
        # 取消密码修改，通过用户个人账户修改或者管理员重置密码方式修改
        # queryset.set_password(password_origin)  # 设置密码
        queryset.save()  # 保存
        '''
        qs = userInfo.objects.filter(id=userid)
        # 判断提交的标签是否包含空标签：当不含空标签，
        if '' not in group_list:
            # 设置标签
            queryset.groups.set(group_list)
            print('1')
        # 判断提交的标签是否包含空标签：当含有空标签，
        else:
            # 清除空元素，设置标签
            group_list.remove('')
            queryset.groups.set(group_list)
            print('2')
        # 判断提交的标签是否包含空标签：当不含空标签，
        if '' not in perm_list:
            # 设置标签
            queryset.user_permissions.set(perm_list)
            print('3')
        # 判断提交的标签是否包含空标签：当含有空标签，
        else:
            # 清除空元素，设置标签
            perm_list.remove('')
            queryset.user_permissions.set(perm_list)
            print('4')
        return redirect('/cmdb/index/table/user/list/')
        # return render_to_response('user.html',msg)
        # return HttpResponse(json.dumps(msg))
    else:
        msg = {'userinfo': userinfo,
               'login_user': user_dict['user'], 'status': '[username, email, ]不能为空',
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=500)


@custom_login_required
@custom_permission_required('myapp.view_userinfo')
def user_detail(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['userid']
    userinfo = userInfo.objects.filter(id=form_id)
    # usergroup = userGroup.objects.filter(id=id)
    userinfo_obj = get_object_or_404(userInfo, pk=form_id)
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
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    perm = Permission.objects.all().exclude(user=userinfo_obj)
    if is_superuser:
        perm_selected = Permission.objects.all()
    else:
        perm_selected = Permission.objects.filter(user=userinfo_obj)

    msg = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'is_staff': is_staff,
           'is_active': is_active,
           'date_joined': date_joined, 'workflow_order': workflow_order, 'password': password, 'last_login': last_login,
           'is_superuser': is_superuser,
           'memo': memo, 'login_user': user_dict['user'], 'status': '操作成功', 'usergroup': usergroup,
           'perm': perm, 'perm_selected': perm_selected, 'userinfo': userinfo, 'group_selected': group_selected,
           'wf_count_pending': wf_dict['wf_count_pending'], }

    # print(msg)
    return render_to_response('account/user_detail.html', msg)


@custom_login_required
def user_change_password(request, *args, **kwargs):
    username = kwargs['username']
    password_origin = request.POST.get('password_origin', None)
    password_new1 = request.POST.get('password_new1', None)
    password_new2 = request.POST.get('password_new2', None)
    update_time = timezone.now()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # is_valid = userInfo.objects.filter(username=username,password=encrypt_helper.md5_encrypt(password_origin)).count()
    # if is_valid != 1:
    # 校验原密码是否输入和数据库一致
    is_valid = userInfo.objects.get(username=username).check_password(password_origin)
    # print(password_origin, password_new1, password_new2)
    # print(is_valid)
    if not is_valid:
        msg = {'status': '原密码输入错误，请重新输入', 'login_user': user_dict['user'], 'code': '1'}
        # return render_to_response('500.html', msg)
    elif not password_new1:
        msg = {'status': '密码不能为空，请重新输入', 'login_user': user_dict['user'], 'code': 2}
    elif password_new1 != password_new2:
        msg = {'status': '两次密码输入不一致，请重新输入', 'login_user': user_dict['user'], 'code': '3'}
        # return render_to_response('500.html',msg)
    else:
        msg = {'status': '密码修改成功', 'login_user': user_dict['user'], 'code': '0',
               'wf_count_pending': wf_dict['wf_count_pending'], }
        # userInfo.objects.filter(username=username).update(password=encrypt_helper.md5_encrypt(password_new2),update_time=update_time,)
        user_obj = get_object_or_404(userInfo, username=username)
        user_obj.set_password(password_new2)
        user_obj.save()
        # return redirect('/cmdb/index/table/user/')
    # return render_to_response('account/settings.html', msg)
    return HttpResponse(json.dumps(msg))


@custom_login_required
# @custom_permission_required('myapp.change_userinfo')
def reset_password(request, *args, **kwargs):
    userid = request.POST.get('userid', None)
    update_time = timezone.now()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # userInfo.objects.filter(id=userid).update(password=encrypt_helper.md5_encrypt('123456'),update_time=update_time,)
    user_obj = get_object_or_404(userInfo, pk=userid)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.change_userinfo'):
        res = user_obj.set_password('password')
        ret = user_obj.save()
        # print(ret, type(ret), res)
        msg = {'login_user': user_dict['user'], 'ret': ret, 'res': res,
               'wf_count_pending': wf_dict['wf_count_pending'], }
        # return render_to_response('account/user.html', msg)
        return JsonResponse(msg)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


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
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # if not userDict:
    #    return redirect('/cmdb/login/')
    msg = {'userinfo': userinfo, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': user_dict['user'],
           'wf_count_pending': wf_dict['wf_count_pending'], }
    response = render_to_response('account/user.html', msg, )
    # response.set_cookie('k1','v1')
    # print(request.COOKIES)
    # print(request.COOKIES.get('page_num'))
    # print(args,kwargs)
    return response


@custom_login_required
# @custom_permission_required('myapp.delete_userinfo')
def user_del(request, *args, **kwargs):
    form_id = request.POST.get('userid')
    username = userInfo.objects.filter(id=form_id).values('username')[0]['username']
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.delete_userinfo'):
        userInfo.objects.filter(id=form_id).delete()
        # print('delete', id)
        msg = {'code': '0', 'status': '删除用户' + username + '成功', }
        return render_to_response('account/user.html', msg)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


@custom_login_required
# @custom_permission_required('myapp.delete_userinfo')
def user_del_all(request, *args, **kwargs):
    array_form_id = request.POST.get('userid')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.delete_userinfo'):
        userInfo.objects.filter(id__in=array_id).delete()
        print('delete', array_id)
        msg = {'code': '0', 'status': '删除用户成功,id列表：' + json.dumps(array_id)}
        print(msg)
        return render_to_response('account/user.html', msg)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


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
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # print(perm)
    msg = {'perm': perm, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'login_user': user_dict['user'],
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('account/permission.html', msg)
