#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
import time
import json
from django.utils.safestring import mark_safe
from apps.myapp import models
from apps.myapp import common
from apps.myapp import page_helper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.template import context
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

#####################################################################################################################################
from django.shortcuts import render, render_to_response, HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
import urllib
import urllib.parse


# Create your views here.

# 添加index函数，用于返回index.html页面


@custom_login_required
@custom_permission_required('myapp.view_devicetype')
def devicetype(request, *args, **kwargs):
    devicetype = models.DeviceType.objects.all()
    count = devicetype.count()
    userDict = request.session.get('is_login', None)
    msg = {'devicetype': devicetype, 'login_user': userDict['user'], 'count': count, }
    return render_to_response('assets/devicetype.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_devicetype')
def devicetypeForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    devicetype = models.DeviceType.objects.all()
    # usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'devicetype': devicetype, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('assets/devicetype_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_devicetype')
def devicetypeAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    # usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = models.userGroup.objects.all()
    # result = {'status': '','usertype':None}
    if request.method == 'POST':
        devicetype = request.POST.get('devicetype', None)
        memo = request.POST.get('memo', None)
        is_exist = models.DeviceType.objects.filter(name=devicetype)
        print(is_exist)
        if not (is_exist):
            is_empty = all([devicetype, ])
            if is_empty:
                models.DeviceType.objects.create(name=devicetype, memo=memo, )
                msg = {'userinfo': userinfo, 'devicetype': devicetype,
                       'login_user': userDict['user'], 'status': '添加设备类型成功', }
                return redirect('/cmdb/index/assets/devicetype/')
            else:
                msg = {'userinfo': userinfo, 'devicetype': devicetype,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            # msg = {'userinfo': userinfo, 'devicetype': devicetype, 'usergroup':usergroup,
            msg = {'userinfo': userinfo, 'devicetype': devicetype,
                   'login_user': userDict['user'], 'status': '该设备类型已存在！', }
    return render_to_response('assets/devicetype_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_devicetype')
def devicetypeForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    devicetype = models.DeviceType.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'devicetype': devicetype, }
    print(msg)
    return render_to_response('assets/devicetype_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_devicetype')
def devicetypeUpdate(request, *args, **kwargs):
    id = kwargs['id']
    devicetype = request.POST.get('devicetype')
    memo = request.POST.get('memo')
    # update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.DeviceType.objects.filter(id=id).update(name=devicetype, memo=memo, )
    return redirect('/cmdb/index/assets/devicetype/')


@custom_login_required
@custom_permission_required('myapp.delete_devicetype')
def devicetypeDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.DeviceType.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除设备类型id:' + id, }
    return render_to_response('assets/devicetype.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_devicestatus')
def devicestatus(request, *args, **kwargs):
    devicestatus = models.DeviceStatus.objects.all()
    count = devicestatus.count()
    userDict = request.session.get('is_login', None)
    msg = {'devicestatus': devicestatus, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/devicestatus.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_devicestatus')
def devicestatusForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    devicestatus = models.DeviceStatus.objects.all()
    # usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'devicestatus': devicestatus, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('assets/devicestatus_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_devicestatus')
def devicestatusAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = models.userGroup.objects.all()
    # result = {'status': '','devicestatus':None}
    if request.method == 'POST':
        devicestatus = request.POST.get('devicestatus', None)
        memo = request.POST.get('memo', None)
        is_exist = models.DeviceStatus.objects.filter(name=devicestatus)
        print(is_exist)
        if not (is_exist):
            is_empty = all([devicestatus, ])
            if is_empty:
                models.DeviceStatus.objects.create(name=devicestatus, memo=memo, )
                msg = {'userinfo': userinfo, 'devicestatus': devicestatus,
                       'login_user': userDict['user'], 'status': '添加设备状态成功', }
                return redirect('/cmdb/index/assets/devicestatus/')
            else:
                msg = {'userinfo': userinfo, 'devicestatus': devicestatus,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            # msg = {'userinfo': userinfo, 'devicestatus': devicestatus, 'usergroup': usergroup,
            msg = {'userinfo': userinfo, 'devicestatus': devicestatus,
                   'login_user': userDict['user'], 'status': '该设备状态已存在！', }
    return render_to_response('assets/devicestatus_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_devicestatus')
def devicestatusForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    devicestatus = models.DeviceStatus.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'devicestatus': devicestatus, }
    print(msg)
    return render_to_response('assets/devicestatus_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_devicestatus')
def devicestatusUpdate(request, *args, **kwargs):
    id = kwargs['id']
    devicestatus = request.POST.get('devicestatus')
    memo = request.POST.get('memo')
    # update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.DeviceStatus.objects.filter(id=id).update(name=devicestatus, memo=memo, )
    return redirect('/cmdb/index/assets/devicestatus/')


@custom_login_required
@custom_permission_required('myapp.delete_devicestatus')
def devicestatusDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.DeviceStatus.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除设备状态id:' + id, }
    return render_to_response('assets/devicestatus.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_idc')
def idc(request, *args, **kwargs):
    idc = models.IDC.objects.all()
    count = idc.count()
    userDict = request.session.get('is_login', None)
    msg = {'idc': idc, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/idc.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_idc')
def idcForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    idc = models.IDC.objects.all()
    # usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'idc': idc, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('assets/idc_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_idc')
def idcAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = models.userGroup.objects.all()
    # result = {'status': '','idc':None}
    if request.method == 'POST':
        idc = request.POST.get('idc', None)
        floor = request.POST.get('floor', None)
        region = request.POST.get('region', None)
        memo = request.POST.get('memo', None)
        is_exist = models.IDC.objects.filter(display_name=idc)
        print(is_exist)
        if not (is_exist):
            is_empty = all([idc, ])
            if is_empty:
                models.IDC.objects.create(display_name=idc, region_display_name=region, floor=floor, memo=memo, )
                msg = {'userinfo': userinfo, 'idc': idc,
                       'login_user': userDict['user'], 'status': '添加idc成功', }
                return redirect('/cmdb/index/assets/idc/')
            else:
                msg = {'userinfo': userinfo, 'idc': idc,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            # msg = {'userinfo': userinfo, 'idc': idc, 'usergroup': usergroup,
            msg = {'userinfo': userinfo, 'idc': idc,
                   'login_user': userDict['user'], 'status': '该idc已存在！', }
    return render_to_response('assets/idc_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_idc')
def idcForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    idc = models.IDC.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'idc': idc, }
    print(msg)
    return render_to_response('assets/idc_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_idc')
def idcUpdate(request, *args, **kwargs):
    id = kwargs['id']
    idc = request.POST.get('idc')
    region = request.POST.get('region', None)
    floor = request.POST.get('floor', None)
    memo = request.POST.get('memo')
    # update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.IDC.objects.filter(id=id).update(display_name=idc, region_display_name=region, floor=floor, memo=memo, )
    return redirect('/cmdb/index/assets/idc/')


@custom_login_required
@custom_permission_required('myapp.delete_idc')
def idcDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.IDC.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除设备状态id:' + id, }
    return render_to_response('assets/idc.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_contract')
def contract(request, *args, **kwargs):
    contract = models.Contract.objects.all()
    count = contract.count()
    userDict = request.session.get('is_login', None)
    msg = {'contract': contract, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/contract.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_contract')
def contractForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    contract = models.Contract.objects.all()
    # usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'contract': contract, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('assets/contract_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_contract')
def contractAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = models.userGroup.objects.all()
    if request.method == 'POST':
        sn = request.POST.get('sn', None)
        name = request.POST.get('name', None)
        cost = request.POST.get('cost', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        license_num = request.POST.get('license_num', None)
        memo = request.POST.get('memo', None)
        is_exist = models.Contract.objects.filter(sn=sn)
        print(is_exist)
        if not (is_exist):
            is_empty = all([sn, ])
            if is_empty:
                models.Contract.objects.create(sn=sn, name=name, cost=cost, start_date=start_date, end_date=end_date,
                                               license_num=license_num, memo=memo, )
                msg = {'userinfo': userinfo, 'contract': contract,
                       'login_user': userDict['user'], 'status': '添加合同成功', }
                return redirect('/cmdb/index/assets/contract/')
            else:
                msg = {'userinfo': userinfo, 'contract': contract,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            # msg = {'userinfo': userinfo, 'contract': contract, 'usergroup': usergroup,
            msg = {'userinfo': userinfo, 'contract': contract,
                   'login_user': userDict['user'], 'status': '该合同已存在！', }
    return render_to_response('assets/contract_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_contract')
def contractForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    contract = models.Contract.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'contract': contract, }
    print(msg)
    return render_to_response('assets/contract_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_contract')
def contractUpdate(request, *args, **kwargs):
    id = kwargs['id']
    sn = request.POST.get('sn', None)
    name = request.POST.get('name', None)
    cost = request.POST.get('cost', None)
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get('end_date', None)
    license_num = request.POST.get('license_num', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.Contract.objects.filter(id=id).update(sn=sn, name=name, cost=cost, start_date=start_date, end_date=end_date,
                                                 license_num=license_num, memo=memo, update_time=update_time, )
    return redirect('/cmdb/index/assets/contract/')


@custom_login_required
@custom_permission_required('myapp.delete_contract')
def contractDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Contract.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除设备状态id:' + id, }
    return render_to_response('assets/contract.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_tag')
def tag(request, *args, **kwargs):
    tag = models.Tag.objects.all()
    count = tag.count()
    userDict = request.session.get('is_login', None)
    msg = {'tag': tag, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/tag.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_tag')
def tagForm_add(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    tag = models.Tag.objects.all()
    # usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'tag': tag, 'login_user': userDict['user'], 'status': '', }
    return render_to_response('assets/tag_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_tag')
def tagAdd(request, *args, **kwargs):
    userinfo = models.userInfo.objects.all()
    userDict = request.session.get('is_login', None)
    # usergroup = models.userGroup.objects.all()
    # result = {'status': '','tag':None}
    if request.method == 'POST':
        tag = request.POST.get('tag', None)
        memo = request.POST.get('memo', None)
        is_exist = models.Tag.objects.filter(name=tag)
        print(is_exist)
        if not (is_exist):
            is_empty = all([tag, ])
            if is_empty:
                models.Tag.objects.create(name=tag, memo=memo, )
                msg = {'userinfo': userinfo, 'tag': tag,
                       'login_user': userDict['user'], 'status': '添加tag成功', }
                return redirect('/cmdb/index/assets/tag/')
            else:
                msg = {'userinfo': userinfo, 'tag': tag,
                       'login_user': userDict['user'], 'status': 'xx不能为空', }
        else:
            # msg = {'userinfo': userinfo, 'tag': tag, 'usergroup': usergroup,
            msg = {'userinfo': userinfo, 'tag': tag,
                   'login_user': userDict['user'], 'status': '该tag已存在！', }
    return render_to_response('assets/tag_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_tag')
def tagForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    tag = models.Tag.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'tag': tag, }
    print(msg)
    return render_to_response('assets/tag_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_tag')
def tagUpdate(request, *args, **kwargs):
    id = kwargs['id']
    tag = request.POST.get('tag')
    memo = request.POST.get('memo')
    # update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.Tag.objects.filter(id=id).update(name=tag, memo=memo, )
    return redirect('/cmdb/index/assets/tag/')


@custom_login_required
@custom_permission_required('myapp.delete_tag')
def tagDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Tag.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除设备状态id:' + id, }
    return render_to_response('assets/tag.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_asset')
def asset(request, *args, **kwargs):
    asset = models.Asset.objects.all()
    count = asset.count()
    userDict = request.session.get('is_login', None)
    msg = {'asset': asset, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/asset.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_asset')
def assetForm_add(request, *args, **kwargs):
    asset = models.Asset.objects.all()
    business_unit = models.wf_business.objects.all()
    userDict = request.session.get('is_login', None)
    device_type = models.DeviceType.objects.all()
    device_status = models.DeviceStatus.objects.all()
    contract = models.Contract.objects.all()
    tag = models.Tag.objects.all()
    idc = models.IDC.objects.all()
    admin = models.userInfo.objects.all()
    msg = {'asset': asset, 'login_user': userDict['user'], 'status': '',
           'device_type': device_type, 'device_status': device_status,
           'contract': contract, 'tag': tag, 'business_unit': business_unit, 'idc': idc, 'admin': admin, }
    return render_to_response('assets/asset_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_asset')
def assetAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        device_type = request.POST.get('device_type', None)
        device_status = request.POST.get('device_status', None)
        contract = request.POST.get('contract', None)
        tag = request.POST.getlist('tag', None)
        business_unit_id = request.POST.get('business_unit', None)
        cabinet_num = request.POST.get('cabinet_num', None)
        cabinet_order = request.POST.get('cabinet_order', None)
        idc = request.POST.get('idc', None)
        admin = request.POST.get('admin', None)
        memo = request.POST.get('memo', None)
        print(tag, )
        is_empty = all([device_type, device_status, ])
        if is_empty:
            queryset = models.Asset.objects.create(device_type_id=device_type, device_status_id=device_status,
                                                   contract_id=contract,
                                                   business_unit_id=business_unit_id, idc_id=idc,
                                                   cabinet_num=cabinet_num,
                                                   cabinet_order=cabinet_order, admin_id=admin, memo=memo, )
            queryset.tag.set(tag)
            msg = {
                'login_user': userDict['user'], 'status': '添加asset成功', }
            return redirect('/cmdb/index/assets/asset/')
        else:
            msg = {
                'login_user': userDict['user'], 'status': 'xx不能为空', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_asset')
def assetForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    asset = models.Asset.objects.filter(id=id)
    print(asset.values_list('tag', flat=True), asset.values_list('tag', flat=True)[0], )
    userDict = request.session.get('is_login', None)
    device_type = models.DeviceType.objects.all().exclude(id=asset.values('device_type')[0]['device_type'])
    device_status = models.DeviceStatus.objects.all().exclude(id=asset.values('device_status')[0]['device_status'])
    contract = models.Contract.objects.all().exclude(id=asset.values('contract')[0]['contract'])
    if (asset.values_list('tag', flat=True)[0] == None):
        tag = models.Tag.objects.all()
    else:
        tag = models.Tag.objects.all().exclude(pk__in=asset.values_list('tag', flat=True))
    print(tag, tag.exists(), )
    business_unit = models.wf_business.objects.all().exclude(id=asset.values('business_unit')[0]['business_unit'])
    idc = models.IDC.objects.all().exclude(id=asset.values('idc')[0]['idc'])
    admin = models.userInfo.objects.all().exclude(id=asset.values('admin')[0]['admin'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'asset': asset,
           'device_type': device_type, 'device_status': device_status,
           'contract': contract, 'tag': tag, 'business_unit': business_unit, 'idc': idc, 'admin': admin, }
    print(msg)
    return render_to_response('assets/asset_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_asset')
def assetUpdate(request, *args, **kwargs):
    id = kwargs['id']
    device_type = request.POST.get('device_type', None)
    device_status = request.POST.get('device_status', None)
    contract = request.POST.get('contract', None)
    tag = request.POST.getlist('tag', None)
    business_unit = request.POST.get('business_unit', None)
    cabinet_num = request.POST.get('cabinet_num', None)
    cabinet_order = request.POST.get('cabinet_order', None)
    idc = request.POST.get('idc', None)
    admin = request.POST.get('admin', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.Asset.objects.filter(id=id).update(device_type_id=device_type, device_status_id=device_status,
                                              contract_id=contract,
                                              business_unit_id=business_unit, idc_id=idc, cabinet_num=cabinet_num,
                                              cabinet_order=cabinet_order, admin_id=admin, memo=memo,
                                              update_time=update_time, )
    queryset = models.Asset.objects.get(id=id)
    queryset.tag.set(tag)
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'asset': asset,
           'device_type': device_type, 'device_status': device_status,
           'contract': contract, 'tag': tag, 'business_unit': business_unit, 'idc': idc, 'admin': admin, }
    print(msg)
    return redirect('/cmdb/index/assets/asset/')


@custom_login_required
@custom_permission_required('myapp.delete_asset')
def assetDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Asset.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除asset id:' + id, }
    return render_to_response('assets/asset.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_host')
def host(request, *args, **kwargs):
    host = models.Server.objects.all()
    count = host.count()
    userDict = request.session.get('is_login', None)
    msg = {'host': host, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/host.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_host')
def hostForm_add(request, *args, **kwargs):
    asset = models.Asset.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'asset': asset, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/host_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_host')
def hostAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        asset = request.POST.get('asset', None)
        hostname = request.POST.get('hostname', None)
        ip = request.POST.get('ip', None)
        sn = request.POST.get('sn', None)
        manufactory = request.POST.get('manufactory', None)
        model = request.POST.get('model', None)
        bios = request.POST.get('bios', None)
        type = request.POST.get('type', None)
        memo = request.POST.get('memo', None)
        print(type, )
        is_exist = models.Server.objects.filter(hostname=hostname, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([asset, hostname, ip, ])
            if is_empty:
                queryset = models.Server.objects.create(asset_id=asset, hostname=hostname, ip=ip, sn=sn,
                                                        manufactory=manufactory,
                                                        model=model, bios=bios, type=type, memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加host成功', }
                return redirect('/cmdb/index/assets/host/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': 'hostname或ip地址已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_host')
def hostForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    host = models.Server.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    asset = models.Asset.objects.all().exclude(id=host.values('asset')[0]['asset'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'host': host, 'asset': asset, }
    print(msg, )
    return render_to_response('assets/host_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_host')
def hostUpdate(request, *args, **kwargs):
    id = kwargs['id']
    asset = request.POST.get('asset', None)
    hostname = request.POST.get('hostname', None)
    ip = request.POST.get('ip', None)
    sn = request.POST.get('sn', None)
    manufactory = request.POST.get('manufactory', None)
    model = request.POST.get('model', None)
    bios = request.POST.get('bios', None)
    type = request.POST.get('type', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.Server.objects.filter(id=id).update(asset_id=asset, hostname=hostname, ip=ip, sn=sn, manufactory=manufactory,
                                               model=model, bios=bios, type=type, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'asset': asset, 'hostname': hostname,
           'sn': sn,
           'manufactory': manufactory, 'model': model, 'bios': bios, 'type': type, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/host/')


@custom_login_required
@custom_permission_required('myapp.delete_host')
def hostDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Server.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除host id:' + id, }
    return render_to_response('assets/host.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_cpu')
def cpu(request, *args, **kwargs):
    cpu = models.CPU.objects.all()
    count = cpu.count()
    userDict = request.session.get('is_login', None)
    msg = {'cpu': cpu, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/cpu.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_cpu')
def cpuForm_add(request, *args, **kwargs):
    host = models.Server.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'host': host, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/cpu_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_cpu')
def cpuAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        server_info = request.POST.get('server_info', None)
        name = request.POST.get('name', None)
        model = request.POST.get('model', None)
        core_num = request.POST.get('core_num', None)
        memo = request.POST.get('memo', None)
        is_exist = models.CPU.objects.filter(name=name, server_info=server_info, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([name, core_num, model, server_info, ])
            if is_empty:
                queryset = models.CPU.objects.create(server_info_id=server_info, name=name,
                                                     model=model, core_num=core_num, memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加cpu成功', }
                return redirect('/cmdb/index/assets/cpu/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': '该CPU name已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_cpu')
def cpuForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    cpu = models.CPU.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    host = models.Server.objects.all().exclude(id=cpu.values('server_info')[0]['server_info'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'cpu': cpu, 'host': host, }
    print(msg, )
    return render_to_response('assets/cpu_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_cpu')
def cpuUpdate(request, *args, **kwargs):
    id = kwargs['id']
    server_info = request.POST.get('server_info', None)
    name = request.POST.get('name', None)
    model = request.POST.get('model', None)
    core_num = request.POST.get('core_num', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.CPU.objects.filter(id=id).update(server_info_id=server_info, name=name,
                                            core_num=core_num, model=model, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'server_info': server_info,
           'name': name, 'core_num': core_num, 'model': model, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/cpu/')


@custom_login_required
@custom_permission_required('myapp.delete_cpu')
def cpuDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.CPU.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除cpu id:' + id, }
    return render_to_response('assets/cpu.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_memory')
def memory(request, *args, **kwargs):
    memory = models.Memory.objects.all()
    count = memory.count()
    userDict = request.session.get('is_login', None)
    msg = {'memory': memory, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/memory.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_memory')
def memoryForm_add(request, *args, **kwargs):
    host = models.Server.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'host': host, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/memory_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_memory')
def memoryAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        server_info = request.POST.get('server_info', None)
        slot = request.POST.get('slot', None)
        model = request.POST.get('model', None)
        capacity = request.POST.get('capacity', None)
        ifac_type = request.POST.get('ifac_type', None)
        memo = request.POST.get('memo', None)
        is_exist = models.Memory.objects.filter(slot=slot, server_info=server_info, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([slot, capacity, ifac_type, model, server_info, ])
            if is_empty:
                queryset = models.Memory.objects.create(server_info_id=server_info, slot=slot,
                                                        ifac_type=ifac_type, model=model, capacity=capacity,
                                                        memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加memory成功', }
                return redirect('/cmdb/index/assets/memory/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': '该memory slot已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_memory')
def memoryForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    memory = models.Memory.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    host = models.Server.objects.all().exclude(id=memory.values('server_info')[0]['server_info'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'memory': memory, 'host': host, }
    print(msg, )
    return render_to_response('assets/memory_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_memory')
def memoryUpdate(request, *args, **kwargs):
    id = kwargs['id']
    server_info = request.POST.get('server_info', None)
    slot = request.POST.get('slot', None)
    model = request.POST.get('model', None)
    capacity = request.POST.get('capacity', None)
    ifac_type = request.POST.get('ifac_type', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.Memory.objects.filter(id=id).update(server_info_id=server_info, slot=slot,
                                               ifac_type=ifac_type, capacity=capacity,
                                               model=model, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'server_info': server_info,
           'slot': slot, 'capacity': capacity, 'ifac_type': ifac_type, 'model': model, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/memory/')


@custom_login_required
@custom_permission_required('myapp.delete_memory')
def memoryDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Memory.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除memory id:' + id, }
    return render_to_response('assets/memory.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_nic')
def nic(request, *args, **kwargs):
    nic = models.NIC.objects.all()
    count = nic.count()
    userDict = request.session.get('is_login', None)
    msg = {'nic': nic, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/nic.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_nic')
def nicForm_add(request, *args, **kwargs):
    host = models.Server.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'host': host, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/nic_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_nic')
def nicAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        server_info = request.POST.get('server_info', None)
        name = request.POST.get('name', None)
        model = request.POST.get('model', None)
        ipaddr = request.POST.get('ipaddr', None)
        mac = request.POST.get('mac', None)
        netmask = request.POST.get('netmask', None)
        memo = request.POST.get('memo', None)
        is_exist = models.NIC.objects.filter(server_info=server_info, name=name, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([name, ipaddr, mac, netmask, model, server_info, ])
            if is_empty:
                queryset = models.NIC.objects.create(server_info_id=server_info, name=name,
                                                     model=model, ipaddr=ipaddr, mac=mac, netmask=netmask, memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加nic成功', }
                return redirect('/cmdb/index/assets/nic/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': '该nic已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_nic')
def nicForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    nic = models.NIC.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    host = models.Server.objects.all().exclude(id=nic.values('server_info')[0]['server_info'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'nic': nic, 'host': host, }
    print(msg, )
    return render_to_response('assets/nic_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_nic')
def nicUpdate(request, *args, **kwargs):
    id = kwargs['id']
    server_info = request.POST.get('server_info', None)
    name = request.POST.get('name', None)
    model = request.POST.get('model', None)
    ipaddr = request.POST.get('ipaddr', None)
    mac = request.POST.get('mac', None)
    netmask = request.POST.get('netmask', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.NIC.objects.filter(id=id).update(server_info_id=server_info, name=name,
                                            ipaddr=ipaddr, mac=mac, netmask=netmask,
                                            model=model, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'server_info': server_info,
           'name': name, 'ipaddr': ipaddr, 'mac': mac, 'netmask': netmask, 'model': model, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/nic/')


@custom_login_required
@custom_permission_required('myapp.delete_nic')
def nicDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.NIC.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除nic id:' + id, }
    return render_to_response('assets/nic.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_disk')
def disk(request, *args, **kwargs):
    disk = models.Disk.objects.all()
    count = disk.count()
    userDict = request.session.get('is_login', None)
    msg = {'disk': disk, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/disk.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_disk')
def diskForm_add(request, *args, **kwargs):
    host = models.Server.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'host': host, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/disk_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_disk')
def diskAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        server_info = request.POST.get('server_info', None)
        slot = request.POST.get('slot', None)
        model = request.POST.get('model', None)
        capacity = request.POST.get('capacity', None)
        ifac_type = request.POST.get('ifac_type', None)
        memo = request.POST.get('memo', None)
        is_exist = models.Disk.objects.filter(slot=slot, server_info=server_info, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([slot, model, capacity, ifac_type, server_info, ])
            if is_empty:
                queryset = models.Disk.objects.create(server_info_id=server_info, slot=slot,
                                                      model=model, capacity=capacity, ifac_type=ifac_type, memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加disk成功', }
                return redirect('/cmdb/index/assets/disk/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': '该disk已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_disk')
def diskForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    disk = models.Disk.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    host = models.Server.objects.all().exclude(id=disk.values('server_info')[0]['server_info'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'disk': disk, 'host': host, }
    print(msg, )
    return render_to_response('assets/disk_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_disk')
def diskUpdate(request, *args, **kwargs):
    id = kwargs['id']
    server_info = request.POST.get('server_info', None)
    slot = request.POST.get('slot', None)
    model = request.POST.get('model', None)
    capacity = request.POST.get('capacity', None)
    ifac_type = request.POST.get('ifac_type', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.Disk.objects.filter(id=id).update(server_info_id=server_info, slot=slot,
                                             capacity=capacity, ifac_type=ifac_type,
                                             model=model, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'server_info': server_info,
           'slot': slot, 'capacity': capacity, 'ifac_type': ifac_type, 'model': model, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/disk/')


@custom_login_required
@custom_permission_required('myapp.delete_disk')
def diskDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.Disk.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除disk id:' + id, }
    return render_to_response('assets/disk.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_networkdevice')
def network(request, *args, **kwargs):
    network = models.NetworkDevice.objects.all()
    count = network.count()
    userDict = request.session.get('is_login', None)
    msg = {'network': network, 'login_user': userDict['user'], 'count': count}
    return render_to_response('assets/network.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_networkdevice')
def networkForm_add(request, *args, **kwargs):
    asset = models.Asset.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'asset': asset, 'login_user': userDict['user'], 'status': '', }
    print(msg, )
    return render_to_response('assets/network_add.html', msg)


@custom_login_required
@custom_permission_required('myapp.add_networkdevice')
def networkAdd(request, *args, **kwargs):
    userDict = request.session.get('is_login', None)
    if request.method == 'POST':
        asset = request.POST.get('asset', None)
        name = request.POST.get('name', None)
        sn = request.POST.get('sn', None)
        manufactory = request.POST.get('manufactory', None)
        model = request.POST.get('model', None)
        memo = request.POST.get('memo', None)
        print(type, )
        is_exist = models.NetworkDevice.objects.filter(sn=sn, )
        print(is_exist)
        if not (is_exist):
            is_empty = all([asset, name, sn, manufactory, model, ])
            if is_empty:
                queryset = models.NetworkDevice.objects.create(asset_id=asset, name=name, sn=sn,
                                                               manufactory=manufactory,
                                                               model=model, memo=memo, )
                msg = {
                    'login_user': userDict['user'], 'status': '添加network成功', }
                return redirect('/cmdb/index/assets/network/')
            else:
                msg = {
                    'login_user': userDict['user'], 'status': 'xx不能为空', }
                return render_to_response('assets/500.html', msg)
        else:
            msg = {
                'login_user': userDict['user'], 'status': '该网络设备已存在', }
            return render_to_response('assets/500.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_networkdevice')
def networkForm_update(request, *args, **kwargs):
    # userid = request.GET.get('userid',None)
    id = kwargs['id']
    network = models.NetworkDevice.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    asset = models.Asset.objects.all().exclude(id=network.values('asset')[0]['asset'])
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'network': network, 'asset': asset, }
    print(msg, )
    return render_to_response('assets/network_update.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_networkdevice')
def networkUpdate(request, *args, **kwargs):
    id = kwargs['id']
    asset = request.POST.get('asset', None)
    name = request.POST.get('name', None)
    sn = request.POST.get('sn', None)
    manufactory = request.POST.get('manufactory', None)
    model = request.POST.get('model', None)
    memo = request.POST.get('memo', None)
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    ##update return value is type int
    models.NetworkDevice.objects.filter(id=id).update(asset_id=asset, name=name, sn=sn, manufactory=manufactory,
                                                      model=model, memo=memo, update_time=update_time, )
    msg = {'id': id, 'login_user': userDict['user'], 'status': '操作成功', 'asset': asset, 'name': name, 'sn': sn,
           'manufactory': manufactory, 'model': model, 'memo': memo, }
    print(msg)
    return redirect('/cmdb/index/assets/network/')


@custom_login_required
@custom_permission_required('myapp.delete_networkdevice')
def networkDel(request, *args, **kwargs):
    id = request.POST.get('id')
    models.NetworkDevice.objects.filter(id=id).delete()
    print('delete', id)
    msg = {'code': 1, 'result': '删除network id:' + id, }
    return render_to_response('assets/network.html', msg)


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
