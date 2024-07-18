#!/usr/bin/env python
# coding:utf-8
import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect

from apps.myapp import common, page_helper
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from apps.myapp import models
from myweb.settings import *


@custom_login_required
@custom_permission_required('myapp.view_oplogs')
def oplog(request, *args, **kwargs):
    op_logs = models.OpLogs.objects.all().order_by('-id')
    count = op_logs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    op_logs_paged = op_logs[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_oplog_list(request, page, pageinfo.pageCount)
    # api_access_timeout = API_ACCESS_TIMEOUT
    # 数据库获取
    api_access_timeout_str = models.SystemConfig.objects.filter(name='default').values('api_access_timeout')[0][
        'api_access_timeout']
    api_access_timeout = int(api_access_timeout_str)
    msg = {'op_logs': op_logs_paged, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'api_access_timeout': api_access_timeout, 'wf_count_pending': wf_dict['wf_count_pending']}
    # return render_to_response('user_search.html',msg)
    return render_to_response('audit/oplog.html', msg)


@custom_login_required
@custom_permission_required('myapp.view_systemconfig')
def system_config(request, *args, **kwargs):
    qs_configs = models.SystemConfig.objects.filter(name='default')
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    msg = {'qs_configs': qs_configs, 'login_user': user_dict['user'], 'status': '操作成功',
           'wf_count_pending': wf_dict['wf_count_pending']}
    # return render_to_response('user_search.html',msg)
    return render_to_response('audit/settings.html', msg)


@custom_login_required
@custom_permission_required('myapp.change_systemconfig')
def system_config_change(request, *args, **kwargs):
    try:
        # Extract data from POST request with default values if necessary
        data = {
            'external_url': request.POST.get('external_url', ''),
            'active_email_subject': request.POST.get('active_email_subject', ''),
            'verify_email_subject': request.POST.get('verify_email_subject', ''),
            'gitlab_url': request.POST.get('gitlab_url', ''),
            'gitlab_token': request.POST.get('gitlab_token', ''),
            'gitlab_job_name': request.POST.get('gitlab_job_name', ''),
            'gitlab_job_name_tomcat': request.POST.get('gitlab_job_name_tomcat', ''),
            'wf_email_subject': request.POST.get('wf_email_subject', ''),
            'skywalking_email_subject': request.POST.get('skywalking_email_subject', ''),
            'skywalking_email_receiver': request.POST.get('skywalking_email_receiver', ''),
            'skywalking_dingtalk_url': request.POST.get('skywalking_dingtalk_url', ''),
            'skywalking_welink_url': request.POST.get('skywalking_welink_url', ''),
            'skywalking_welink_uuid': request.POST.get('skywalking_welink_uuid', ''),
            'prom_dingtalk_url': request.POST.get('prom_dingtalk_url', ''),
            'prom_welink_url': request.POST.get('prom_welink_url', ''),
            'prom_welink_uuid': request.POST.get('prom_welink_uuid', ''),
            'deploy_dingtalk_url': request.POST.get('deploy_dingtalk_url', ''),
            'deploy_welink_url': request.POST.get('deploy_welink_url', ''),
            'deploy_welink_uuid': request.POST.get('deploy_welink_uuid', ''),
            'ansible_base_dir': request.POST.get('ansible_base_dir', ''),
            'tomcat_project_list': request.POST.get('tomcat_project_list', ''),
            'grafana_url': request.POST.get('grafana_url', ''),
            'skywalking_ui_url': request.POST.get('skywalking_ui_url', ''),
            'api_access_timeout': request.POST.get('api_access_timeout', '')
        }

        print(data)

        # Fetch user and workflow information from session
        user_dict = request.session.get('is_login', {})
        wf_dict = request.session.get('wf', {})

        # Update the SystemConfig model
        models.SystemConfig.objects.filter(name='default').update(**data)

        # Prepare the response message
        msg = {
            'status': '修改成功',
            'login_user': user_dict.get('user', ''),
            'code': '0',
            'wf_count_pending': wf_dict.get('wf_count_pending', 0)
        }
        return JsonResponse(msg)

    except ObjectDoesNotExist:
        return JsonResponse({'status': '修改失败', 'code': '1', 'message': 'System configuration not found'},
                            status=404)
    except Exception as e:
        return JsonResponse({'status': '修改失败', 'code': '1', 'message': str(e)}, status=500)


@custom_login_required
@custom_permission_required('myapp.view_oplogs')
def oplog_search(request, *args, **kwargs):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    page = '1'
    print(start_time, type(start_time))
    print(end_time, type(end_time))
    is_empty = all([start_time, end_time])
    if is_empty:
        return redirect('/cmdb/index/audit/oplog/search_result/start_time=' + start_time + '&end_time=' + end_time + '&page=' + page)
        # return redirect(reverse("account.search_result", kwargs={"keyword": keyword, "page": page}))
    else:
        return redirect('/cmdb/index/audit/oplog/list/')
        # return redirect(reverse("account.user", kwargs={"page": page}))


@custom_login_required
@custom_permission_required('myapp.view_oplogs')
def oplog_search_result(request, *args, **kwargs):
    start_time = kwargs['start_time']
    end_time = kwargs['end_time']
    start_time_fmt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_time_fmt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    print(start_time_fmt, type(start_time_fmt))
    print(end_time_fmt, type(end_time_fmt))
    op_logs = models.OpLogs.objects.filter(re_time__range=(start_time_fmt, end_time_fmt))
    print(op_logs)
    count = op_logs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo_search_by_time(page, count, perItem, start_time, end_time)
    op_logs = op_logs[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_oplog_list_search(request, page, pageinfo.pageCount, start_time, end_time)
    msg = {'op_logs': op_logs, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'wf_count_pending': wf_dict['wf_count_pending'], }
    # return render_to_response('user_search.html',msg)
    return render_to_response('audit/oplog.html', msg)
