#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from apps.myapp import views
from apps.myapp import zabbix
from apps.myapp import mygitlab
from apps.myapp import prometheus
from apps.myapp import workflow
from apps.myapp import example

from apps.myapp import tasks
#######################################################################################
from rest_framework import routers
from apps.myapp import api


urlpatterns=[
    path('index/layout/normal/', example.layoutsnormal),
    path('index/layout/fixed-sidebar/', example.layoutsfixedsidebar),
    path('index/layout/fixed-header/', example.layoutsfixedheader),
    path('index/layout/hide-sidebar/', example.layoutshiddensidebar),
    path('index/ui/alert/', example.uialerts),
    path('index/ui/button/', example.uibuttons),
    path('index/ui/card/', example.uicards),
    path('index/ui/modal/', example.uimodals),
    path('index/ui/tab/', example.uitabs),
    path('index/ui/progress-bar/', example.uiprogressbars),
    path('index/ui/widget/', example.uiwidgets),
    path('index/chart/js/', example.chartjs),
    path('index/form/', example.forms),
    path('index/tables/', example.tables),
    path('index/page/login/', example.pagelogin),
    path('index/page/register/', example.pageregister),
    path('index/page/invoice/', example.pageinvoice),
    path('index/page/404/', example.page404),
    path('index/page/500/', example.page500),
    path('index/page/set/', example.pageset),
    path('index/page/blank/', example.pageblank),


path('',views.cmdb),
path('login/',views.login),
path('logout/',views.logout),
path('login/auth/', views.auth),
path('register/', views.register),
url('^register/active/token=(?P<token>\w+)', views.active),
path('index/',views.index),
path('login/forget_pass/step/1/',views.forget_pass_form_1),
path('login/forget_pass/step/2/',views.forget_pass_form_2),
url(r'^login/forget_pass/send/',views.forget_pass_send),
#url(r'^login/forget_pass/send/email=(?P<email>\w+@(\w+\.\w+)+)',views.forget_pass_send),
path('login/forget_pass/change/',views.forget_pass_change),

path('index/table/usertype/',views.usertype),
path('index/table/usergroup/',views.usergroup),

path('index/table/user/form_add/',views.userForm_add),
path('index/table/usertype/form_add/',views.usertypeForm_add),
path('index/table/usergroup/form_add/',views.usergroupForm_add),

#path('index/table/user/form_update/',views.userForm_update),
url(r'^index/table/user/form_update/userid=(?P<userid>\d*)',views.userForm_update),
url(r'^index/table/usertype/form_update/id=(?P<id>\d*)',views.usertypeForm_update),
url(r'^index/table/usergroup/form_update/id=(?P<id>\d*)',views.usergroupForm_update),

path('index/table/user/add/',views.userAdd),
path('index/table/usertype/add/',views.usertypeAdd),
path('index/table/usergroup/add/',views.usergroupAdd),

url(r'^index/table/user/update/userid=(?P<userid>\d*)',views.userUpdate),
url(r'^index/table/usertype/update/id=(?P<id>\d*)',views.usertypeUpdate),
url(r'^index/table/usergroup/update/id=(?P<id>\d*)',views.usergroupUpdate),

path('index/table/user/del/',views.userDel),
path('index/table/usertype/del/',views.usertypeDel),
path('index/table/usergroup/del/',views.usergroupDel),

    url('^index/table/user/search/',views.search),
url('^index/table/user/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',views.search_result),
    path('index/monitor/zabbix/',zabbix.zabbix_trigger),
path('index/monitor/gitlab/', mygitlab.git_project),
    path('index/monitor/prometheus/', prometheus.prometheus_alert),
    #path('index/table/',views.tables),
    #url(r'^index/table/(\d*)',views.tables),
url(r'^index/table/user/(?P<page>\d*)',views.tables),


path('index/wf/list/',workflow.wf),
url(r'^index/wf/detail/',workflow.workflow_detail),
path('index/wf/requests/form_add/',workflow.wrokflow_form_add),
path('index/wf/requests/add/',workflow.workflow_add),
url(r'^index/wf/requests/form_update/sn=(?P<sn>\w+)',workflow.workflow_form_update),

url(r'^index/wf/requests/update/sn=(?P<sn>\w+)',workflow.workflow_update),
path('index/wf/requests/list/',workflow.workflow_requests),
url(r'^index/wf/requests/detail/',workflow.workflow_detail),
path('index/wf/upload/',workflow.workflow_upload),
url(r'^index/wf/requests/commit/sn=(?P<sn>\w+)',workflow.workflow_commit),
url(r'^index/wf/requests/withdraw/sn=(?P<sn>\w+)',workflow.workflow_withdraw),
path('index/wf/tasks/list/',workflow.workflow_tasks),
url(r'^index/wf/tasks/detail/',workflow.workflow_detail),
url(r'^index/wf/tasks/approve/',workflow.workflow_approve),
path('index/wf/tasks/process/',workflow.workflow_process),

path('index/wf/wftype/',workflow.wftype),
path('index/wf/wftype/form_add/',workflow.wftypeForm_add),
url(r'^index/wf/wftype/form_update/id=(?P<id>\d*)',workflow.wftypeForm_update),
path('index/wf/wftype/add/',workflow.wftypeAdd),
url(r'^index/wf/wftype/update/id=(?P<id>\d*)',workflow.wftypeUpdate),
path('index/wf/wftype/del/',workflow.wftypeDel),

path('index/wf/wfbusiness/',workflow.wfbusiness),
path('index/wf/wfbusiness/ajax/',workflow.wfbusiness_ajax),
path('index/wf/wfbusiness/form_add/',workflow.wfbusinessForm_add),
url(r'^index/wf/wfbusiness/form_update/id=(?P<id>\d*)',workflow.wfbusinessForm_update),
url(r'^index/wf/wfbusiness/form_deploy/id=(?P<id>\d*)',workflow.wfbusinessForm_deploy),
path('index/wf/wfbusiness/add/',workflow.wfbusinessAdd),
url(r'^index/wf/wfbusiness/update/id=(?P<id>\d*)',workflow.wfbusinessUpdate),
path('index/wf/wfbusiness/del/',workflow.wfbusinessDel),
path('index/wf/wfbusiness/deploy/del/',workflow.wfbusiness_deploy_del),
url(r'^index/wf/wfbusiness/deploy/id=(?P<id>\d*)',workflow.wfbusiness_deploy),
url(r'^index/wf/wfbusiness/deploy/log/id=(?P<id>\d*)',workflow.wfbusiness_deploy_log),
path('index/wf/wfbusiness/deploy/list/',workflow.wfbusiness_deploy_list),


################################################################################################################################
#url(r'^', include(router.urls)),

    url(r'^serverinfo/', views.serverinfo),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]