#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from apps.myapp import views
from apps.myapp import zabbix
from apps.myapp import gitlab_helper
from apps.myapp import prometheus
from apps.myapp import workflow
from apps.myapp import example
from apps.myapp import assets
from apps.myapp import deploy

from apps.myapp import tasks
#######################################################################################
from rest_framework import routers
#from apps.myapp import api


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

###---------- login------------------###
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

###---------- permission------------------###
    path('index/permission/list/',views.permission),

###---------- users------------------###
    path('index/table/usergroup/',views.usergroup),
    path('index/table/user/form_add/',views.userForm_add),
    path('index/table/usergroup/form_add/',views.usergroupForm_add),
    #path('index/table/user/form_update/',views.userForm_update),
    url(r'^index/table/user/form_update/userid=(?P<userid>\d*)',views.userForm_update),
    url(r'^index/table/user/form_change_password/username=(?P<username>\w+)',views.userForm_change_password),
    url(r'^index/table/user/form_get_profile/username=(?P<username>\w+)',views.userForm_get_profile),
    url(r'^index/table/usergroup/form_update/id=(?P<id>\d*)',views.usergroupForm_update),
    path('index/table/user/add/',views.userAdd),
    path('index/table/usergroup/add/',views.usergroupAdd),
    url(r'^index/table/user/update/userid=(?P<userid>\d*)',views.userUpdate),
    url(r'^index/table/user/change_password/username=(?P<username>\w+)',views.user_change_password),
    url(r'^index/table/usergroup/update/id=(?P<id>\d*)',views.usergroupUpdate),
    path('index/table/user/del/',views.userDel),
    path('index/table/user/resetPwd/',views.resetPwd),
    path('index/table/usergroup/del/',views.usergroupDel),
    url('^index/table/user/search/',views.search),
    url('^index/table/user/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',views.search_result),
    url(r'^index/table/user/(?P<page>\d*)',views.user),


###---------- assets------------------###
    path('index/assets/devicetype/',assets.devicetype),
    path('index/assets/devicetype/form_add/',assets.devicetypeForm_add),
    path('index/assets/devicetype/add/',assets.devicetypeAdd),
    url(r'^index/assets/devicetype/form_update/id=(?P<id>\d*)',assets.devicetypeForm_update),
    url(r'^index/assets/devicetype/update/id=(?P<id>\d*)',assets.devicetypeUpdate),
    path('index/assets/devicetype/del/',assets.devicetypeDel),
    path('index/assets/devicestatus/',assets.devicestatus),
    path('index/assets/devicestatus/form_add/',assets.devicestatusForm_add),
    path('index/assets/devicestatus/add/',assets.devicestatusAdd),
    url(r'^index/assets/devicestatus/form_update/id=(?P<id>\d*)',assets.devicestatusForm_update),
    url(r'^index/assets/devicestatus/update/id=(?P<id>\d*)',assets.devicestatusUpdate),
    path('index/assets/devicestatus/del/',assets.devicestatusDel),
    path('index/assets/idc/',assets.idc),
    path('index/assets/idc/form_add/',assets.idcForm_add),
    path('index/assets/idc/add/',assets.idcAdd),
    url(r'^index/assets/idc/form_update/id=(?P<id>\d*)',assets.idcForm_update),
    url(r'^index/assets/idc/update/id=(?P<id>\d*)',assets.idcUpdate),
    path('index/assets/idc/del/',assets.idcDel),
    path('index/assets/contract/',assets.contract),
    path('index/assets/contract/form_add/',assets.contractForm_add),
    path('index/assets/contract/add/',assets.contractAdd),
    url(r'^index/assets/contract/form_update/id=(?P<id>\d*)',assets.contractForm_update),
    url(r'^index/assets/contract/update/id=(?P<id>\d*)',assets.contractUpdate),
    path('index/assets/contract/del/',assets.contractDel),
    path('index/assets/tag/',assets.tag),
    path('index/assets/tag/form_add/',assets.tagForm_add),
    path('index/assets/tag/add/',assets.tagAdd),
    url(r'^index/assets/tag/form_update/id=(?P<id>\d*)',assets.tagForm_update),
    url(r'^index/assets/tag/update/id=(?P<id>\d*)',assets.tagUpdate),
    path('index/assets/tag/del/',assets.tagDel),
    path('index/assets/asset/',assets.asset),
    path('index/assets/asset/form_add/',assets.assetForm_add),
    path('index/assets/asset/add/',assets.assetAdd),
    url(r'^index/assets/asset/form_update/id=(?P<id>\d*)',assets.assetForm_update),
    url(r'^index/assets/asset/update/id=(?P<id>\d*)',assets.assetUpdate),
    path('index/assets/asset/del/',assets.assetDel),
    path('index/assets/host/',assets.host),
    path('index/assets/host/form_add/',assets.hostForm_add),
    path('index/assets/host/add/',assets.hostAdd),
    url(r'^index/assets/host/form_update/id=(?P<id>\d*)',assets.hostForm_update),
    url(r'^index/assets/host/update/id=(?P<id>\d*)',assets.hostUpdate),
    path('index/assets/host/del/',assets.hostDel),
    path('index/assets/cpu/',assets.cpu),
    path('index/assets/cpu/form_add/',assets.cpuForm_add),
    path('index/assets/cpu/add/',assets.cpuAdd),
    url(r'^index/assets/cpu/form_update/id=(?P<id>\d*)',assets.cpuForm_update),
    url(r'^index/assets/cpu/update/id=(?P<id>\d*)',assets.cpuUpdate),
    path('index/assets/cpu/del/',assets.cpuDel),
    path('index/assets/memory/',assets.memory),
    path('index/assets/memory/form_add/',assets.memoryForm_add),
    path('index/assets/memory/add/',assets.memoryAdd),
    url(r'^index/assets/memory/form_update/id=(?P<id>\d*)',assets.memoryForm_update),
    url(r'^index/assets/memory/update/id=(?P<id>\d*)',assets.memoryUpdate),
    path('index/assets/memory/del/',assets.memoryDel),
    path('index/assets/nic/',assets.nic),
    path('index/assets/nic/form_add/',assets.nicForm_add),
    path('index/assets/nic/add/',assets.nicAdd),
    url(r'^index/assets/nic/form_update/id=(?P<id>\d*)',assets.nicForm_update),
    url(r'^index/assets/nic/update/id=(?P<id>\d*)',assets.nicUpdate),
    path('index/assets/nic/del/',assets.nicDel),
    path('index/assets/disk/',assets.disk),
    path('index/assets/disk/form_add/',assets.diskForm_add),
    path('index/assets/disk/add/',assets.diskAdd),
    url(r'^index/assets/disk/form_update/id=(?P<id>\d*)',assets.diskForm_update),
    url(r'^index/assets/disk/update/id=(?P<id>\d*)',assets.diskUpdate),
    path('index/assets/disk/del/',assets.diskDel),
    path('index/assets/network/',assets.network),
    path('index/assets/network/form_add/',assets.networkForm_add),
    path('index/assets/network/add/',assets.networkAdd),
    url(r'^index/assets/network/form_update/id=(?P<id>\d*)',assets.networkForm_update),
    url(r'^index/assets/network/update/id=(?P<id>\d*)',assets.networkUpdate),
    path('index/assets/network/del/',assets.networkDel),
###---------- monitor------------------###
    path('index/monitor/zabbix/',zabbix.zabbix_trigger),
    path('index/monitor/gitlab/', gitlab_helper.git_project),
    path('index/monitor/prometheus/', prometheus.prometheus_alert),
    #path('index/table/',views.tables),
    #url(r'^index/table/(\d*)',views.tables),

###---------- workflow------------------###
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
    path('index/wf/wfbusiness/add/',workflow.wfbusinessAdd),
    url(r'^index/wf/wfbusiness/update/id=(?P<id>\d*)',workflow.wfbusinessUpdate),
    path('index/wf/wfbusiness/del/',workflow.wfbusinessDel),
###---------- deploy------------------###
    url(r'^index/wf/wfbusiness/form_deploy/id=(?P<id>\d*)',deploy.wfbusinessForm_deploy),
    path('index/wf/wfbusiness/deploy/del/',deploy.wfbusiness_deploy_del),
    url(r'^index/wf/wfbusiness/deploy/id=(?P<id>\d*)',deploy.wfbusiness_deploy),
    url(r'^index/wf/wfbusiness/deploy/log/id=(?P<id>\d*)',deploy.wfbusiness_deploy_log),
    path('index/wf/wfbusiness/deploy/list/',deploy.wfbusiness_deploy_list),
    path('index/script/scripttype/',deploy.scripttype),
    path('index/script/scripttype/form_add/',deploy.scripttypeForm_add),
    url(r'^index/script/scripttype/form_update/id=(?P<id>\d*)',deploy.scripttypeForm_update),
    path('index/script/scripttype/add/',deploy.scripttypeAdd),
    url(r'^index/script/scripttype/update/id=(?P<id>\d*)',deploy.scripttypeUpdate),
    path('index/script/scripttype/del/',deploy.scripttypeDel),


################################################################################################################################
    #url(r'^', include(router.urls)),

    url(r'^serverinfo/', views.serverinfo),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]