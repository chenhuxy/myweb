#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import webbrowser
from datetime import datetime

from django.http import JsonResponse

from myweb.settings import *

import requests
from django.db.models import Q

from django.shortcuts import redirect, get_object_or_404
import time
import json
from django.utils.safestring import mark_safe
from apps.myapp import models, common, page_helper, excel_helper

from django.utils import timezone

from apps.myapp.auth_helper import custom_login_required, custom_permission_required

from django.shortcuts import render, render_to_response, HttpResponse


# Create your views here.

# 添加index函数，用于返回index.html页面


@custom_login_required
@custom_permission_required('myapp.view_assetenvtype')
def env_type(request, *args, **kwargs):
    qs = models.AssetEnvType.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'env_type': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/env_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetenvtype')
def env_type_form_add(request, *args, **kwargs):
    qs = models.AssetEnvType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'env_type': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/env_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetenvtype')
def env_type_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        env_type_name = request.POST.get('env_type', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetEnvType.objects.filter(name=env_type_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([env_type_name, ])
            if is_empty:
                models.AssetEnvType.objects.create(name=env_type_name, memo=memo, )
                msg = {'env_type_name': env_type_name,
                       'login_user': user_dict['user'], 'status': '添加环境类型成功', }
                return redirect('/cmdb/index/assets/env-type/list/')
            else:
                msg = {'env_type_name': env_type_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'env_type_name': env_type_name,
                   'login_user': user_dict['user'], 'status': '该环境类型已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/env_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetenvtype')
def env_type_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetEnvType.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'env_type': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/env_type_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetenvtype')
def env_type_update(request, *args, **kwargs):
    form_id = kwargs['id']
    env_type_name = request.POST.get('env_type')
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetEnvType.objects.filter(id=form_id).update(name=env_type_name, memo=memo, )
    return redirect('/cmdb/index/assets/env-type/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assetenvtype')
def env_type_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetEnvType.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除环境类型成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/env_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_assetostype')
def os_type(request, *args, **kwargs):
    qs = models.AssetOsType.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'os_type': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/os_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetostype')
def os_type_form_add(request, *args, **kwargs):
    qs = models.AssetOsType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'os_type': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/os_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetostype')
def os_type_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        os_type_name = request.POST.get('os_type', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetOsType.objects.filter(name=os_type_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([os_type_name, ])
            if is_empty:
                models.AssetOsType.objects.create(name=os_type_name, memo=memo, )
                msg = {'os_type_name': os_type_name,
                       'login_user': user_dict['user'], 'status': '添加操作系统类型成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/os-type/list/')
            else:
                msg = {'os_type_name': os_type_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'os_type_name': os_type_name,
                   'login_user': user_dict['user'], 'status': '该操作系统类型已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/os_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetostype')
def os_type_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetOsType.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'os_type': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/os_type_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetostype')
def os_type_update(request, *args, **kwargs):
    form_id = kwargs['id']
    os_type_name = request.POST.get('os_type')
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetOsType.objects.filter(id=form_id).update(name=os_type_name, memo=memo, )
    return redirect('/cmdb/index/assets/os-type/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assetostype')
def os_type_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetOsType.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除操作系统类型成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/os_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_assetdevicetype')
def device_type(request, *args, **kwargs):
    qs = models.AssetDeviceType.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'device_type': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetdevicetype')
def device_type_form_add(request, *args, **kwargs):
    qs = models.AssetDeviceType.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'device_type': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetdevicetype')
def device_type_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        device_type_name = request.POST.get('device_type', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetDeviceType.objects.filter(name=device_type_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([device_type_name, ])
            if is_empty:
                models.AssetDeviceType.objects.create(name=device_type_name, memo=memo, )
                msg = {'device_type_name': device_type_name,
                       'login_user': user_dict['user'], 'status': '添加设备类型成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/device-type/list/')
            else:
                msg = {'device_type_name': device_type_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'device_type_name': device_type_name,
                   'login_user': user_dict['user'], 'status': '该设备类型已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_type_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetdevicetype')
def device_type_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetDeviceType.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'device_type': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/device_type_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetdevicetype')
def device_type_update(request, *args, **kwargs):
    form_id = kwargs['id']
    device_type_name = request.POST.get('device_type')
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetDeviceType.objects.filter(id=form_id).update(name=device_type_name, memo=memo, )
    return redirect('/cmdb/index/assets/device-type/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assetdevicetype')
def device_type_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetDeviceType.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除设备类型成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/device_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_assetdevicestatus')
def device_status(request, *args, **kwargs):
    qs = models.AssetDeviceStatus.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'device_status': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_status.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetdevicestatus')
def device_status_form_add(request, *args, **kwargs):
    qs = models.AssetDeviceStatus.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'device_status': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_status_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetdevicestatus')
def device_status_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        device_status_name = request.POST.get('device_status', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetDeviceStatus.objects.filter(name=device_status_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([device_status_name, ])
            if is_empty:
                models.AssetDeviceStatus.objects.create(name=device_status_name, memo=memo, )
                msg = {'device_status': device_status_name,
                       'login_user': user_dict['user'], 'status': '添加设备状态成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/device-status/list/')
            else:
                msg = {'device_status': device_status_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'device_status': device_status_name,
                   'login_user': user_dict['user'], 'status': '该设备状态已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/device_status_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetdevicestatus')
def device_status_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetDeviceStatus.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'device_status': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/device_status_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetdevicestatus')
def device_status_update(request, *args, **kwargs):
    form_id = kwargs['id']
    device_status_name = request.POST.get('device_status')
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetDeviceStatus.objects.filter(id=form_id).update(name=device_status_name, memo=memo, )
    return redirect('/cmdb/index/assets/device-status/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assetdevicestatus')
def device_status_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetDeviceStatus.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除设备状态成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/device_type.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_assetidc')
def idc(request, *args, **kwargs):
    qs = models.AssetIDC.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'idc': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/idc.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetidc')
def idc_form_add(request, *args, **kwargs):
    qs = models.AssetIDC.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'idc': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/idc_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assetidc')
def idc_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        idc_name = request.POST.get('idc', None)
        floor = request.POST.get('floor', None)
        region = request.POST.get('region', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetIDC.objects.filter(display_name=idc_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([idc_name, ])
            if is_empty:
                models.AssetIDC.objects.create(display_name=idc_name, region_display_name=region, floor=floor,
                                               memo=memo, )
                msg = {'idc': idc_name,
                       'login_user': user_dict['user'], 'status': '添加idc成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/idc/list/')
            else:
                msg = {'idc': idc_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'idc': idc_name,
                   'login_user': user_dict['user'], 'status': '该idc已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/idc_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetidc')
def idc_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetIDC.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'idc': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/idc_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assetidc')
def idc_update(request, *args, **kwargs):
    form_id = kwargs['id']
    idc_name = request.POST.get('idc')
    region = request.POST.get('region', None)
    floor = request.POST.get('floor', None)
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetIDC.objects.filter(id=form_id).update(display_name=idc_name, region_display_name=region,
                                                      floor=floor, memo=memo, )
    return redirect('/cmdb/index/assets/idc/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assetidc')
def idc_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetIDC.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除idc成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/idc.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_assettag')
def tag(request, *args, **kwargs):
    qs = models.AssetTag.objects.all()
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'tag': qs, 'login_user': user_dict['user'], 'count': count,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/tag.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assettag')
def tag_form_add(request, *args, **kwargs):
    qs = models.AssetTag.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'tag': qs, 'login_user': user_dict['user'], 'status': '',
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/tag_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_assettag')
def tag_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        tag_name = request.POST.get('tag', None)
        memo = request.POST.get('memo', None)
        is_exist = models.AssetTag.objects.filter(name=tag_name)
        print(is_exist)
        if not is_exist:
            is_empty = all([tag_name, ])
            if is_empty:
                models.AssetTag.objects.create(name=tag_name, memo=memo, )
                msg = {'tag': tag_name,
                       'login_user': user_dict['user'], 'status': '添加tag成功',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/tag/list/')
            else:
                msg = {'tag': tag_name,
                       'login_user': user_dict['user'], 'status': '名称不能为空',
                       'wf_count_pending': wf_dict['wf_count_pending'], }
        else:
            msg = {'tag': tag_name,
                   'login_user': user_dict['user'], 'status': '该tag已存在！',
                   'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/tag_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assettag')
def tag_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.AssetTag.objects.filter(id=form_id)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'tag': qs,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    print(msg)
    return render_to_response('assets/tag_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_assettag')
def tag_update(request, *args, **kwargs):
    form_id = kwargs['id']
    tag_name = request.POST.get('tag')
    memo = request.POST.get('memo')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    models.AssetTag.objects.filter(id=form_id).update(name=tag_name, memo=memo, )
    return redirect('/cmdb/index/assets/tag/list/')


@custom_login_required
@custom_permission_required('myapp.delete_assettag')
def tag_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.AssetTag.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除tag成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/tag.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset(request, *args, **kwargs):
    qs = models.Asset.objects.all()
    count = qs.count()
    page = common.try_int(kwargs['page'], 1)
    per_item = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, per_item)
    qs_paged = qs[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_assets_asset_list(request, page, pageinfo.pageCount)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'asset': qs_paged, 'login_user': user_dict['user'], 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string, 'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/asset.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset_detail(request, *args, **kwargs):
    form_id = kwargs['id']
    qs = models.Asset.objects.filter(id=form_id)
    asset_obj = get_object_or_404(models.Asset, pk=form_id)
    tag_list = models.AssetTag.objects.filter(asset=asset_obj)
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'login_user': user_dict['user'], 'status': '操作成功', 'assets': qs, 'tag': tag_list,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # print(msg)
    return render_to_response('assets/asset_detail.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_asset')
def asset_form_add(request, *args, **kwargs):
    qs = models.Asset.objects.all()
    business_unit = models.wf_business.objects.all()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    qs_device_type = models.AssetDeviceType.objects.all()
    qs_device_status = models.AssetDeviceStatus.objects.all()
    qs_tag = models.AssetTag.objects.all()
    qs_idc = models.AssetIDC.objects.all()
    qs_admin = models.userInfo.objects.all()
    qs_env = models.AssetEnvType.objects.all()
    qs_os = models.AssetOsType.objects.all()
    qs_ansible_vars = models.AnsibleVars.objects.all()
    msg = {'asset': qs, 'login_user': user_dict['user'], 'status': '',
           'device_type': qs_device_type, 'device_status': qs_device_status,
           'tag': qs_tag, 'business_unit': business_unit, 'idc': qs_idc,
           'admin': qs_admin, 'env_type': qs_env, 'os_type': qs_os,
           'wf_count_pending': wf_dict['wf_count_pending'],
           'ansible_vars': qs_ansible_vars, }
    return render_to_response('assets/asset_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_asset')
def asset_add(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        ip = request.POST.get('ip', None)
        device_type_id = request.POST.get('device_type', None)
        device_status_id = request.POST.get('device_status', None)
        env_type_id = request.POST.get('env_type', None)
        os_type_id = request.POST.get('os_type', None)
        business_unit_id = request.POST.get('business_unit', None)
        tag_list = request.POST.getlist('tag', None)
        cabinet_num = request.POST.get('cabinet_num', None)
        cabinet_order = request.POST.get('cabinet_order', None)
        idc_id = request.POST.get('idc', None)
        admin_id = request.POST.get('admin', None)
        hostname = request.POST.get('hostname', None)
        sn = request.POST.get('sn', None)
        resource_size = request.POST.get('resource_size', None)
        disk_size = request.POST.get('disk_size', None)
        manufactory = request.POST.get('manufactory', None)
        model = request.POST.get('model', None)
        bios = request.POST.get('bios', None)
        is_docker = request.POST.get('is_docker', None)
        memo = request.POST.get('memo', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        external_ip = request.POST.get('external_ip', None)
        ansible_vars_id = request.POST.get('ansible_vars', None)
        print(tag_list, )
        # required_filed = [ip, device_type_id, device_status_id, env_type_id, os_type_id, business_unit_id]
        required_filed = [ip, ]
        is_empty = all(required_filed)
        if is_empty:
            is_exist = models.Asset.objects.filter(ip=ip)
            print(is_exist)
            if not is_exist:
                queryset = models.Asset.objects.create(ip=ip, device_type_id=device_type_id,
                                                       device_status_id=device_status_id, env_type_id=env_type_id,
                                                       os_type_id=os_type_id, business_unit_id=business_unit_id,
                                                       cabinet_num=cabinet_num, cabinet_order=cabinet_order,
                                                       idc_id=idc_id, admin_id=admin_id, hostname=hostname,
                                                       sn=sn, manufactory=manufactory, model=model, bios=bios,
                                                       is_docker=is_docker, memo=memo, resource_size=resource_size,
                                                       disk_size=disk_size, username=username, password=password,
                                                       external_ip=external_ip, ansible_vars_id=ansible_vars_id)
                # 判断提交的标签是否包含空标签：当不含空标签，
                if '' not in tag_list:
                    # 设置标签
                    queryset.tag.set(tag_list)
                    print('1')
                # 判断提交的标签是否包含空标签：当含有空标签，
                else:
                    # 清除空元素，设置标签
                    tag_list.remove('')
                    queryset.tag.set(tag_list)
                    print('2')
                msg = {
                    'login_user': user_dict['user'], 'status': '添加asset成功',
                    'wf_count_pending': wf_dict['wf_count_pending'], }
                return redirect('/cmdb/index/assets/asset/list/')
            else:
                msg = {
                    'login_user': user_dict['user'], 'status': 'ip地址已存在',
                    'wf_count_pending': wf_dict['wf_count_pending'], }
                return render_to_response('500.html', msg, status=500)
        else:
            msg = {
                'login_user': user_dict['user'], 'status': '[ip,]不能为空',
                'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=500)

    else:
        msg = {
            'login_user': user_dict['user'], 'status': '使用POST方法',
            'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=500)


@custom_login_required
# @custom_permission_required('myapp.add_asset')
def asset_upload(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    # 2024/5/7 增加是否具有权限的判断
    login_user_obj = get_object_or_404(models.userInfo, username=user_dict['user'])
    if login_user_obj.has_perm('myapp.add_asset'):
        if request.method == 'POST':

            files = request.FILES.get('mf', None)
            # save_files = os.path.join("F:\\upload", files.name)
            # 240627 增加目录是否存在判断
            import_dir = "static/import"
            if not os.path.exists(import_dir):
                os.makedirs(import_dir)
            save_files = os.path.join(import_dir, files.name)
            print(files, type(files))
            with open(save_files, 'wb+') as f:
                for line in files:
                    f.write(line)
            data = excel_helper.read_excel(save_files, 'asset')
            count = 0
            count_success = 0
            count_fail = 0
            # print(data, type(data))
            result = []
            for item in data:
                print(item, type(item))
                is_blank = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '']
                is_title = ['实例数据', '', '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', '', '', '', '', '', '']
                # print(is_blank, type(is_blank), is_title, type(is_title))
                # print(item != is_blank, item != is_title)
                if item != is_blank and item != is_title:
                    count = count + 1
                    # required_filed = [ip, device_type_id, device_status_id, env_type_id, os_type_id, business_unit_id]
                    required_filed = [item[5], ]
                    is_empty = all(required_filed)
                    if is_empty:
                        is_exist = models.Asset.objects.filter(ip=item[5])
                        # print(is_exist)
                        if not is_exist:
                            queryset = models.Asset.objects.create(ip=item[5], device_type_id=item[19],
                                                                   device_status_id=item[18], env_type_id=item[20],
                                                                   os_type_id=item[22], business_unit_id=item[17],
                                                                   cabinet_num=item[1], cabinet_order=item[2],
                                                                   idc_id=item[21], admin_id=item[16], hostname=item[4],
                                                                   sn=item[6], manufactory=item[7], model=item[8],
                                                                   bios=item[9], is_docker=item[12], memo=item[3],
                                                                   resource_size=item[13], disk_size=item[14],
                                                                   username=item[10], password=item[11],
                                                                   external_ip=item[15])
                            # queryset.tag.set(item[22])

                            count_success = count_success + 1
                            status = '添加asset成功：' + item[5]
                            result.append(status)
                            # return redirect('/cmdb/index/assets/asset/list/')
                        else:
                            count_fail = count_fail + 1
                            status = 'ip地址已存在：' + item[5]
                            result.append(status)
                            # return render_to_response('500.html', msg)
                    else:
                        count_fail = count_fail + 1
                        status = '第' + str(data.index(item)) + '行：[ip,]不能为空'
                        result.append(status)
            msg = {'login_user': user_dict['user'], 'result': result, 'count': count, 'count_success': count_success,
                   'count_fail': count_fail, 'wf_count_pending': wf_dict['wf_count_pending'], }
            print(msg)
            return HttpResponse(json.dumps(msg))

        else:
            msg = {
                'login_user': user_dict['user'], 'status': '使用POST方法',
                'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=405)
    else:
        msg = {'login_user': user_dict['user'],
               'wf_count_pending': wf_dict['wf_count_pending'], }
        return JsonResponse(msg, status=403)


@custom_login_required
@custom_permission_required('myapp.change_asset')
def asset_form_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    form_id = kwargs['id']
    qs = models.Asset.objects.filter(id=form_id)
    # print(qs.values_list('tag', flat=True), qs.values_list('tag', flat=True)[0], )
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    qs_device_type = models.AssetDeviceType.objects.all().exclude(id=qs.values('device_type')[0]['device_type'])
    qs_device_status = models.AssetDeviceStatus.objects.all().exclude(id=qs.values('device_status')[0]['device_status'])
    qs_env_type = models.AssetEnvType.objects.all().exclude(id=qs.values('env_type')[0]['env_type'])
    qs_os_type = models.AssetOsType.objects.all().exclude(id=qs.values('os_type')[0]['os_type'])
    qs_ansible_vars = models.AnsibleVars.objects.all().exclude(id=qs.values('ansible_vars')[0]['ansible_vars'])
    if qs.values_list('tag', flat=True)[0] is None:
        tag_list = models.AssetTag.objects.all()
    else:
        tag_list = models.AssetTag.objects.all().exclude(pk__in=qs.values_list('tag', flat=True))
    # print(tag_list, tag_list.exists(), )
    business_unit = models.wf_business.objects.all().exclude(id=qs.values('business_unit')[0]['business_unit'])
    qs_idc = models.AssetIDC.objects.all().exclude(id=qs.values('idc')[0]['idc'])
    admin = models.userInfo.objects.all().exclude(id=qs.values('admin')[0]['admin'])
    msg = {'id': form_id, 'login_user': user_dict['user'], 'status': '操作成功', 'asset': qs,
           'device_type': qs_device_type, 'device_status': qs_device_status, 'env_type': qs_env_type,
           'os_type': qs_os_type,
           'tag': tag_list, 'business_unit': business_unit, 'idc': qs_idc, 'admin': admin,
           'wf_count_pending': wf_dict['wf_count_pending'], 'ansible_vars': qs_ansible_vars}
    # print(msg)
    return render_to_response('assets/asset_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_asset')
def asset_update(request, *args, **kwargs):
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    if request.method == 'POST':
        form_id = kwargs['id']
        qs = models.Asset.objects.filter(id=form_id)
        queryset = models.Asset.objects.get(id=form_id)
        print(qs.values_list('tag', flat=True), qs.values_list('tag', flat=True)[0], )
        ip = request.POST.get('ip', None)
        device_type_id = request.POST.get('device_type', None)
        device_status_id = request.POST.get('device_status', None)
        env_type_id = request.POST.get('env_type', None)
        os_type_id = request.POST.get('os_type', None)
        business_unit_id = request.POST.get('business_unit', None)
        tag_list = request.POST.getlist('tag', None)
        cabinet_num = request.POST.get('cabinet_num', None)
        cabinet_order = request.POST.get('cabinet_order', None)
        idc_id = request.POST.get('idc', None)
        admin_id = request.POST.get('admin', None)
        hostname = request.POST.get('hostname', None)
        sn = request.POST.get('sn', None)
        resource_size = request.POST.get('resource_size', None)
        disk_size = request.POST.get('disk_size', None)
        manufactory = request.POST.get('manufactory', None)
        model = request.POST.get('model', None)
        bios = request.POST.get('bios', None)
        is_docker = request.POST.get('is_docker', None)
        memo = request.POST.get('memo', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        external_ip = request.POST.get('external_ip', None)
        update_time = timezone.now()
        ansible_vars_id = request.POST.get('ansible_vars', None)
        print(tag_list, )
        # required_filed = [ip, device_type_id, device_status_id, env_type_id, os_type_id, business_unit_id]
        required_filed = [ip, ]
        is_empty = all(required_filed)
        if is_empty:
            # update return value is type int
            qs.update(ip=ip, device_type_id=device_type_id, device_status_id=device_status_id, env_type_id=env_type_id,
                      os_type_id=os_type_id, business_unit_id=business_unit_id, cabinet_num=cabinet_num,
                      cabinet_order=cabinet_order, idc_id=idc_id, admin_id=admin_id, hostname=hostname,
                      sn=sn, manufactory=manufactory, model=model, bios=bios, is_docker=is_docker, memo=memo,
                      resource_size=resource_size, disk_size=disk_size, username=username, password=password,
                      external_ip=external_ip, update_time=update_time, ansible_vars_id=ansible_vars_id)
            # 判断提交的标签是否包含空标签：当不含空标签，
            if '' not in tag_list:
                # 设置标签
                queryset.tag.set(tag_list)
                print('1')
            # 判断提交的标签是否包含空标签：当含有空标签，
            else:
                # 清除空元素，设置标签
                tag_list.remove('')
                queryset.tag.set(tag_list)
                print('2')
            msg = {
                'login_user': user_dict['user'], 'status': '更新asset成功',
                'wf_count_pending': wf_dict['wf_count_pending'], }
            # print(msg)
            return redirect('/cmdb/index/assets/asset/list/')
        else:
            msg = {
                'login_user': user_dict['user'], 'status': '[ip, device_type_id, device_status_id, env_type_id, '
                                                           'os_type_id, business_unit_id]不能为空',
                'wf_count_pending': wf_dict['wf_count_pending'], }
            return render_to_response('500.html', msg, status=500)

    else:
        msg = {
            'login_user': user_dict['user'], 'status': '使用POST方法',
            'wf_count_pending': wf_dict['wf_count_pending'], }
        return render_to_response('500.html', msg, status=405)


@custom_login_required
@custom_permission_required('myapp.delete_asset')
def asset_del(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    models.Asset.objects.filter(id__in=array_id).delete()
    print('delete', array_id)
    msg = {'code': '0', 'status': '删除asset成功,id列表：' + json.dumps(array_id)}
    print(msg)
    return render_to_response('assets/asset.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset_export(request, *args, **kwargs):
    array_form_id = request.POST.get('id')
    array_id = json.loads(array_form_id)
    print(array_form_id, type(array_form_id))
    print(array_id, type(array_id))
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y%m%d%H%M%S')
    # export_dir = "D:\\BaiduNetdiskWorkspace\myweb-master\static\export"
    # 240627 增加目录是否存在判断
    export_dir = "static/export"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    file_name = "export_asset_" + formatted_time + ".xls"
    export_files = os.path.join(export_dir, file_name)
    # 数据写入excel
    data_list = []
    # 插入表头
    data_title = ['机柜号', '机架号', '备注', '主机名', 'ip地址 *', 'SN号', '厂商', '型号', 'BIOS', '用户名', '密码',
                  'docker环境', '资源配置', '磁盘配置', '外网ip地址', '设备管理员', '所属业务线',
                  '设备状态', '设备类型', '业务环境类型', 'idc机房', '系统类型', '创建时间', '修改时间',
                  ]
    data_field = ['cabinet_num', 'cabinet_order', 'memo', 'hostname', 'ip', 'sn', 'manufactory', 'model', 'bios',
                  'username', 'password', 'is_docker', 'resource_size', 'disk_size', 'external_ip', 'admin_id',
                  'business_unit_id',
                  'device_status_id', 'device_type_id', 'env_type_id', 'idc_id', 'os_type_id', 'create_time',
                  'update_time',
                  ]
    data_list.append(data_title)
    # 插入数据
    for row_num in range(1, len(array_id) + 1):
        qs_asset_obj = models.Asset.objects.filter(id=array_id[row_num - 1])
        data_row = []

        for col_num in range(len(data_field) - 9):
            data_row.append(qs_asset_obj.values(data_field[col_num])[0][data_field[col_num]])
        '''
        for col_num in range(len(data_field) - 9, len(data_field) - 2):
            print(qs_asset_obj.values(data_field[col_num])[0][data_field[col_num]])
            print(models.userInfo.objects.filter(
                    id=qs_asset_obj.values(data_field[col_num])[0][data_field[col_num]]
                ))
        '''
        if qs_asset_obj.values('admin_id')[0]['admin_id'] is not None:
            data_row.append(
                models.userInfo.objects.filter(
                    id=qs_asset_obj.values('admin_id')[0]['admin_id']
                ).values('username')[0]['username']
            )
        else:
            data_row.append('')
        if qs_asset_obj.values('business_unit_id')[0]['business_unit_id'] is not None:
            data_row.append(
                models.wf_business.objects.filter(
                    id=qs_asset_obj.values('business_unit_id')[0]['business_unit_id']
                ).values('name')[0]['name'])
        else:
            data_row.append('')
        if qs_asset_obj.values('device_status_id')[0]['device_status_id'] is not None:
            data_row.append(
                models.AssetDeviceStatus.objects.filter(
                    id=qs_asset_obj.values('device_status_id')[0]['device_status_id']
                ).values('name')[0]['name'])
        else:
            data_row.append('')
        if qs_asset_obj.values('device_type_id')[0]['device_type_id'] is not None:
            data_row.append(
                models.AssetDeviceType.objects.filter(
                    id=qs_asset_obj.values('device_type_id')[0]['device_type_id']
                ).values('name')[0]['name'])
        else:
            data_row.append('')
        if qs_asset_obj.values('env_type_id')[0]['env_type_id'] is not None:
            data_row.append(
                models.AssetEnvType.objects.filter(
                    id=qs_asset_obj.values('env_type_id')[0]['env_type_id']
                ).values('name')[0]['name'])
        else:
            data_row.append('')
        if qs_asset_obj.values('idc_id')[0]['idc_id'] is not None:
            data_row.append(
                models.AssetIDC.objects.filter(
                    id=qs_asset_obj.values('idc_id')[0]['idc_id']
                ).values('display_name')[0]['display_name'])
        else:
            data_row.append('')
        if qs_asset_obj.values('os_type_id')[0]['os_type_id'] is not None:
            data_row.append(
                models.AssetOsType.objects.filter(
                    id=qs_asset_obj.values('os_type_id')[0]['os_type_id']
                ).values('name')[0]['name'])
        else:
            data_row.append('')

        for col_num in range(len(data_field) - 2, len(data_field)):
            data_row.append(qs_asset_obj.values(data_field[col_num])[0][data_field[col_num]])
        data_list.append(data_row)
        # print(data_list)
        # print(row_num)
    for row_num in range(len(data_list)):
        excel_helper.write_excel(export_files, 'asset', row_num, data_list[row_num])
    # 下载导出的excel
    # 数据库获取
    external_url = models.SystemConfig.objects.filter(name='default').values('external_url')[0][
        'external_url']
    url = external_url + '/cmdb/static/export/' + file_name

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 '
    }

    try:
        webbrowser.open(url, new=0)
        print(f"File downloaded successfully and saved as {file_name}")
    except webbrowser.Error as e:
        webbrowser.open(url, new=2)
        print(f"Error downloading the file: {e}")
    """
    try:
        with requests.get(url, stream=True, headers=headers, timeout=30) as response:
            response.raise_for_status()
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"File downloaded successfully and saved as {file_name}")
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")
    """

    msg = {'code': '0', 'status': '写入数据成功,id列表：' + json.dumps(array_id)}
    # print(msg)

    return render_to_response('assets/asset.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset_search(request, *args, **kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    # print(keyword, page)
    if keyword:
        return redirect('/cmdb/index/assets/asset/search_result/keyword=' + keyword + '&page=' + page)
        # return redirect(reverse("account.search_result", kwargs={"keyword": keyword, "page": page}))
    else:
        return redirect('/cmdb/index/assets/asset/list/')
        # return redirect(reverse("account.user", kwargs={"page": page}))


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset_search_result(request, *args, **kwargs):
    keyword = kwargs['keyword']
    qs = models.Asset.objects.filter(ip__icontains=keyword) | models.Asset.objects.filter(
        hostname__icontains=keyword) | models.Asset.objects.filter(
        sn__icontains=keyword) | models.Asset.objects.filter(memo__icontains=keyword)
    count = qs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    per_item = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search(page, count, per_item, keyword)
    qs_paged = qs[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_user_list_search(request, page, pageinfo.pageCount, keyword)
    msg = {'asset': qs_paged, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    return render_to_response('assets/asset.html', msg)


"""
@custom_login_required
@custom_permission_required('myapp.view_wf_business')
def business(request, *args, **kwargs):
    business = models.business.objects.all()
    count = business.count()
    userDict = request.session.get('is_login', None)
    msg = {'business': business, 'login_user': userDict['user'], 'count': count, }
    return render_to_response('assets/business.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def businessForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    business = models.business.objects.all()
    # usergroup = models.userGroup.objects.all()
    approval = userinfo.exclude(workflow_order=0)
    userDict = request.session.get('is_login', None)
    msg = {'business': business, 'userinfo': userinfo,
           'login_user': userDict['user'], 'status': '', 'approval': approval, }
    print(msg)
    return render_to_response('assets/business_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_wf_business')
def businessAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        business = request.POST.get('business', None)
        admin_id = request.POST.get('admin', None)
        is_exist = models.business.objects.filter(name=business)
        print(is_exist)
        if not (is_exist):
            is_empty = all([business, ])
            if is_empty:
                queryset = models.business.objects.create(name=business, admin_id=admin_id, )
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': userDict['user'], 'status': '添加业务单元成功', }
                return redirect('/cmdb/index/wf/deploy/business/')
            else:
                msg = {'userinfo': userinfo, 'business': business,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'business': business,
                   'login_user': userDict['user'], 'status': '该业务单元已存在！', }
    return render_to_response('assets/business_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def businessForm_update(request, *args, **kwargs):
    id = kwargs['id']
    business = models.business.objects.filter(id=id)
    admin = models.userInfo.objects.all().exclude(unit_admin__id=id)
    approval = models.userInfo.objects.all().exclude(workflow_order=0).exclude(approval__id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': u'操作成功', 'business': business,
           'admin': admin, 'approval': approval, }
    print(msg)
    return render_to_response('assets/business_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def businessUpdate(request, *args, **kwargs):
    id = kwargs['id']
    business = request.POST.get('business')
    admin_id = request.POST.get('admin')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.business.objects.filter(id=id).update(name=business,
                                                 update_time=update_time, admin_id=admin_id, )
    return redirect('/cmdb/index/wf/deploy/business/')


@custom_login_required
@custom_permission_required('myapp.change_wf_business')
def business_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            business_id = request.POST.get('business', None)
            print(business_id)
            business = models.business.objects.filter(id=business_id)
            director_id = business.values('director_id')[0]['director_id']
            director = models.userInfo.objects.filter(id=director_id).values('username')[0]['username']
            print(business, director_id, director, )
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
@custom_permission_required('myapp.delete_wf_business')
def businessDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.business.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除工单类型id:' + id, }
    return render_to_response('assets/business.html', msg)
"""
