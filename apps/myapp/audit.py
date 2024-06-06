#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render_to_response

from apps.myapp import common, page_helper
from apps.myapp.auth_helper import custom_login_required, custom_permission_required
from apps.myapp.models import OpLogs
from myweb.settings import API_ACCESS_TIMEOUT


@custom_login_required
@custom_permission_required('myapp.view_oplogs')
def oplog(request, *args, **kwargs):
    op_logs = OpLogs.objects.all().order_by('-id')
    count = op_logs.count()
    user_dict = request.session.get('is_login', None)
    wf_dict = request.session.get('wf', None)
    page = common.try_int(kwargs['page'], 1)
    # print(keyword, page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = page_helper.pageinfo(page, count, perItem)
    op_logs_paged = op_logs[pageinfo.start:pageinfo.end]
    page_string = page_helper.pager_oplog_list(request, page, pageinfo.pageCount)
    msg = {'op_logs': op_logs_paged, 'login_user': user_dict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string,
           'api_access_timeout': API_ACCESS_TIMEOUT, 'wf_count_pending': wf_dict['wf_count_pending']}
    # return render_to_response('user_search.html',msg)
    return render_to_response('audit/oplog.html', msg)
