#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.urls import path
from django.conf.urls import url, include
from apps.myapp import account
from apps.myapp import zabbix
from apps.myapp import gitlab_helper
from apps.myapp import prometheus
from apps.myapp import workflow
from apps.myapp import example
from apps.myapp import assets
from apps.myapp import deploy
from apps.myapp import skywalking
from apps.myapp import audit

# from rest_framework import routers
# from apps.myapp import api


urlpatterns = [

    # audit-------------------------------------------------------------------------------------------------------------
    url(r'^index/audit/oplog/list/(?P<page>\d*)', audit.oplog, ),

    # login-------------------------------------------------------------------------------------------------------------

    path('', account.cmdb, ),
    path('login/', account.login, ),
    path('logout/', account.logout, ),
    path('login/auth/', account.auth, ),
    path('register/', account.register, ),
    url(r'^register/active/token=(?P<token>\w+)', account.active, ),
    path('index/', account.index, ),
    path('login/forget_pass/step/1/', account.forget_pass_form_1, ),
    path('login/forget_pass/step/2/', account.forget_pass_form_2, ),
    url(r'^login/forget_pass/send/', account.forget_pass_send, ),
    # url(r'^login/forget_pass/send/email=(?P<email>\w+@(\w+\.\w+)+)',account.forget_pass_send),
    path('login/forget_pass/change/', account.forget_pass_change, ),

    # permission--------------------------------------------------------------------------------------------------------

    url(r'index/permission/list/(?P<page>\d*)', account.permission, ),

    # users-------------------------------------------------------------------------------------------------------------

    path('index/table/usergroup/list/', account.usergroup, ),
    path('index/table/user/form_add/', account.userForm_add, ),
    path('index/table/usergroup/form_add/', account.usergroupForm_add, ),
    # path('index/table/user/form_update/',account.userForm_update),
    url(r'^index/table/user/form_update/userid=(?P<userid>\d*)', account.userForm_update,
        ),
    url(r'^index/table/user/form_change_password/username=(?P<username>\w+)', account.userForm_change_password,
        ),
    url(r'^index/table/user/form_get_profile/username=(?P<username>\w+)', account.userForm_get_profile,
        ),
    url(r'^index/table/usergroup/form_update/id=(?P<id>\d*)', account.usergroupForm_update,
        ),
    path('index/table/user/add/', account.userAdd, ),
    path('index/table/usergroup/add/', account.usergroupAdd, ),
    url(r'^index/table/user/update/userid=(?P<userid>\d*)', account.userUpdate, ),
    url(r'^index/table/user/show_detail/userid=(?P<userid>\d*)', account.userDetail, ),
    url(r'^index/table/user/change_password/username=(?P<username>\w+)', account.user_change_password,
        ),
    url(r'^index/table/usergroup/update/id=(?P<id>\d*)', account.usergroupUpdate, ),
    url(r'^index/table/usergroup/show_detail/id=(?P<id>\d*)', account.usergroupDetail, ),
    path('index/table/user/del/', account.userDel, ),
    path('index/table/user/resetPwd/', account.resetPwd, ),
    path('index/table/usergroup/del/', account.usergroupDel, ),
    url(r'^index/table/user/search/', account.search, ),
    url(r'^index/table/user/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)', account.search_result,
        ),
    url(r'^index/table/user/list/(?P<page>\d*)', account.user, ),

    # monitor-----------------------------------------------------------------------------------------------------------

    path('index/monitor/zabbix/alert/list/', zabbix.zabbix_trigger, ),
    path('index/monitor/skywalking/alert/send/', skywalking.send_alert, ),
    path('index/monitor/prometheus/alert/send/', prometheus.send_alert, ),
    path('index/monitor/gitlab/', gitlab_helper.git_project, ),
    url(r'^index/monitor/prometheus/alert/list/(?P<page>\d*)', prometheus.prometheus_alert,
        ),
    # path('index/table/',views.tables),
    # url(r'^index/table/(\d*)',views.tables),

    # workflow----------------------------------------------------------------------------------------------------------

    url(r'^index/wf/list/(?P<page>\d*)', workflow.wf, ),
    url(r'^index/wf/search/', workflow.wf_search, ),
    url(r'^index/wf/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)', workflow.wf_search_result, ),
    url(r'^index/wf/detail/', workflow.workflow_detail, ),
    path('index/wf/requests/form_add/', workflow.wrokflow_form_add, ),
    path('index/wf/requests/add/', workflow.workflow_add, ),
    path('index/wf/requests/add/api/', workflow.workflow_add_api, ),
    url(r'^index/wf/requests/search/', workflow.workflow_requests_search, ),
    url(r'^index/wf/requests/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',
        workflow.workflow_requests_search_result, ),
    url(r'^index/wf/requests/form_update/sn=(?P<sn>\w+)', workflow.workflow_form_update, ),
    url(r'^index/wf/requests/update/sn=(?P<sn>\w+)', workflow.workflow_update, ),
    url(r'^index/wf/requests/list/(?P<page>\d*)', workflow.workflow_requests, ),
    url(r'^index/wf/requests/detail/', workflow.workflow_detail, ),
    path('index/wf/upload/', workflow.workflow_upload, ),
    url(r'^index/wf/requests/commit/sn=(?P<sn>\w+)', workflow.workflow_commit, ),
    url(r'^index/wf/requests/withdraw/sn=(?P<sn>\w+)', workflow.workflow_withdraw, ),
    url(r'^index/wf/tasks/list/(?P<page>\d*)', workflow.workflow_tasks, ),
    url(r'^index/wf/tasks/detail/', workflow.workflow_detail, ),
    url(r'^index/wf/tasks/approve/', workflow.workflow_approve, ),
    url(r'^index/wf/tasks/get_task_status/', workflow.workflow_tasks_status, ),
    path('index/wf/tasks/process/', workflow.workflow_process, ),
    path('index/wf/wftype/list/', workflow.wftype, ),
    path('index/wf/wftype/form_add/', workflow.wftypeForm_add, ),
    url(r'^index/wf/wftype/form_update/id=(?P<id>\d*)', workflow.wftypeForm_update, ),
    path('index/wf/wftype/add/', workflow.wftypeAdd, ),
    url(r'^index/wf/wftype/update/id=(?P<id>\d*)', workflow.wftypeUpdate, ),
    path('index/wf/wftype/del/', workflow.wftypeDel, ),
    path('index/wf/wftype/change/', workflow.wftypeChange, ),
    path('index/wf/wftype/change2/', workflow.wftypeChange2, ),

    path('index/wf/wfbusiness/list/', workflow.wfbusiness, ),
    # path('index/deploy/wfbusiness/ajax/',deploy.wfbusiness_ajax),
    path('index/wf/wfbusiness/form_add/', workflow.wfbusiness_form_add, ),
    url(r'^index/wf/wfbusiness/form_update/id=(?P<id>\d*)', workflow.wfbusiness_form_update, ),
    path('index/wf/wfbusiness/add/', workflow.wfbusiness_add, ),
    url(r'^index/wf/wfbusiness/update/id=(?P<id>\d*)', workflow.wfbusiness_update, ),
    path('index/wf/wfbusiness/del/', workflow.wfbusiness_del, ),

    # task-deploy-------------------------------------------------------------------------------------------------------

    path('index/deploy/sum/', deploy.deploy_sum, ),
    path('index/deploy/sum/yearly/', deploy.deploy_sum_yearly, ),
    path('index/deploy/scripttype/list/', deploy.deploy_script_type, ),
    path('index/deploy/scripttype/form_add/', deploy.deploy_script_type_form_add, ),
    url(r'^index/deploy/scripttype/form_update/id=(?P<id>\d*)', deploy.deploy_script_type_form_update, ),
    path('index/deploy/scripttype/add/', deploy.deploy_script_type_add, ),
    url(r'^index/deploy/scripttype/update/id=(?P<id>\d*)', deploy.deploy_script_type_update, ),
    path('index/deploy/scripttype/del/', deploy.deploy_script_type_del, ),

    url(r'^index/deploy/app/list/(?P<page>\d*)', deploy.deploy_app, ),
    url(r'^index/deploy/app/search/', deploy.deploy_app_search, ),
    url(r'^index/deploy/app/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',
        deploy.deploy_app_search_result, ),
    # path('index/wf/deploy/ajax/', deploy.deploy_ajax),
    path('index/deploy/app/form_add/', deploy.deploy_app_form_add, ),
    url(r'^index/deploy/app/form_update/id=(?P<id>\d*)', deploy.deploy_app_form_update, ),
    path('index/deploy/app/add/', deploy.deploy_app_add, ),
    url(r'^index/deploy/app/update/id=(?P<id>\d*)', deploy.deploy_app_update, ),
    path('index/deploy/app/del/', deploy.deploy_app_del, ),

    url(r'^index/deploy/task/form_add/id=(?P<id>\d*)', deploy.deploy_list_form_add, ),
    path('index/deploy/task/add/', deploy.deploy_list_add, ),
    url(r'index/deploy/task/list/(?P<page>\d*)', deploy.deploy_list, ),
    url(r'^index/deploy/task/search/', deploy.deploy_list_search, ),
    url(r'^index/deploy/task/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',
        deploy.deploy_list_search_result, ),
    url(r'^index/deploy/task/log/id=(?P<id>\d*)', deploy.deploy_list_log, ),
    url(r'^index/deploy/task/cancel/id=(?P<id>\d*)', deploy.deploy_list_cancel, ),
    # url(r'^index/wf/deploy/get_task_log/', deploy.get_task_log),
    # url(r'^index/wf/deploy/get_task_status/', deploy.get_task_status),
    url(r'^index/deploy/task/get_task_info/', deploy.get_task_info, ),

    # example-----------------------------------------------------------------------------------------------------------

    path('index/layout/normal/', example.layoutsnormal, ),
    path('index/layout/fixed-sidebar/', example.layoutsfixedsidebar, ),
    path('index/layout/fixed-header/', example.layoutsfixedheader, ),
    path('index/layout/hide-sidebar/', example.layoutshiddensidebar, ),
    path('index/ui/alert/', example.uialerts, ),
    path('index/ui/button/', example.uibuttons, ),
    path('index/ui/card/', example.uicards, ),
    path('index/ui/modal/', example.uimodals, ),
    path('index/ui/tab/', example.uitabs, ),
    path('index/ui/progress-bar/', example.uiprogressbars, ),
    path('index/ui/widget/', example.uiwidgets, ),
    path('index/chart/js/', example.chartjs, ),
    path('index/form/', example.forms, ),
    path('index/tables/', example.tables, ),
    path('index/page/login/', example.pagelogin, ),
    path('index/page/register/', example.pageregister, ),
    path('index/page/invoice/', example.pageinvoice, ),
    path('index/page/404/', example.page404, ),
    path('index/page/500/', example.page500, ),
    path('index/page/set/', example.pageset, ),
    path('index/page/blank/', example.pageblank, ),

    # assets------------------------------------------------------------------------------------------------------------

    path('index/assets/devicetype/', assets.devicetype),
    path('index/assets/devicetype/form_add/', assets.devicetypeForm_add),
    path('index/assets/devicetype/add/', assets.devicetypeAdd),
    url(r'^index/assets/devicetype/form_update/id=(?P<id>\d*)', assets.devicetypeForm_update),
    url(r'^index/assets/devicetype/update/id=(?P<id>\d*)', assets.devicetypeUpdate),
    path('index/assets/devicetype/del/', assets.devicetypeDel),
    path('index/assets/devicestatus/', assets.devicestatus),
    path('index/assets/devicestatus/form_add/', assets.devicestatusForm_add),
    path('index/assets/devicestatus/add/', assets.devicestatusAdd),
    url(r'^index/assets/devicestatus/form_update/id=(?P<id>\d*)', assets.devicestatusForm_update),
    url(r'^index/assets/devicestatus/update/id=(?P<id>\d*)', assets.devicestatusUpdate),
    path('index/assets/devicestatus/del/', assets.devicestatusDel),
    path('index/assets/idc/', assets.idc),
    path('index/assets/idc/form_add/', assets.idcForm_add),
    path('index/assets/idc/add/', assets.idcAdd),
    url(r'^index/assets/idc/form_update/id=(?P<id>\d*)', assets.idcForm_update),
    url(r'^index/assets/idc/update/id=(?P<id>\d*)', assets.idcUpdate),
    path('index/assets/idc/del/', assets.idcDel),
    path('index/assets/contract/', assets.contract),
    path('index/assets/contract/form_add/', assets.contractForm_add),
    path('index/assets/contract/add/', assets.contractAdd),
    url(r'^index/assets/contract/form_update/id=(?P<id>\d*)', assets.contractForm_update),
    url(r'^index/assets/contract/update/id=(?P<id>\d*)', assets.contractUpdate),
    path('index/assets/contract/del/', assets.contractDel),
    path('index/assets/tag/', assets.tag),
    path('index/assets/tag/form_add/', assets.tagForm_add),
    path('index/assets/tag/add/', assets.tagAdd),
    url(r'^index/assets/tag/form_update/id=(?P<id>\d*)', assets.tagForm_update),
    url(r'^index/assets/tag/update/id=(?P<id>\d*)', assets.tagUpdate),
    path('index/assets/tag/del/', assets.tagDel),
    path('index/assets/asset/', assets.asset),
    path('index/assets/asset/form_add/', assets.assetForm_add),
    path('index/assets/asset/add/', assets.assetAdd),
    url(r'^index/assets/asset/form_update/id=(?P<id>\d*)', assets.assetForm_update),
    url(r'^index/assets/asset/update/id=(?P<id>\d*)', assets.assetUpdate),
    path('index/assets/asset/del/', assets.assetDel),
    path('index/assets/host/', assets.host),
    path('index/assets/host/form_add/', assets.hostForm_add),
    path('index/assets/host/add/', assets.hostAdd),
    url(r'^index/assets/host/form_update/id=(?P<id>\d*)', assets.hostForm_update),
    url(r'^index/assets/host/update/id=(?P<id>\d*)', assets.hostUpdate),
    path('index/assets/host/del/', assets.hostDel),
    path('index/assets/cpu/', assets.cpu),
    path('index/assets/cpu/form_add/', assets.cpuForm_add),
    path('index/assets/cpu/add/', assets.cpuAdd),
    url(r'^index/assets/cpu/form_update/id=(?P<id>\d*)', assets.cpuForm_update),
    url(r'^index/assets/cpu/update/id=(?P<id>\d*)', assets.cpuUpdate),
    path('index/assets/cpu/del/', assets.cpuDel),
    path('index/assets/memory/', assets.memory),
    path('index/assets/memory/form_add/', assets.memoryForm_add),
    path('index/assets/memory/add/', assets.memoryAdd),
    url(r'^index/assets/memory/form_update/id=(?P<id>\d*)', assets.memoryForm_update),
    url(r'^index/assets/memory/update/id=(?P<id>\d*)', assets.memoryUpdate),
    path('index/assets/memory/del/', assets.memoryDel),
    path('index/assets/nic/', assets.nic),
    path('index/assets/nic/form_add/', assets.nicForm_add),
    path('index/assets/nic/add/', assets.nicAdd),
    url(r'^index/assets/nic/form_update/id=(?P<id>\d*)', assets.nicForm_update),
    url(r'^index/assets/nic/update/id=(?P<id>\d*)', assets.nicUpdate),
    path('index/assets/nic/del/', assets.nicDel),
    path('index/assets/disk/', assets.disk),
    path('index/assets/disk/form_add/', assets.diskForm_add),
    path('index/assets/disk/add/', assets.diskAdd),
    url(r'^index/assets/disk/form_update/id=(?P<id>\d*)', assets.diskForm_update),
    url(r'^index/assets/disk/update/id=(?P<id>\d*)', assets.diskUpdate),
    path('index/assets/disk/del/', assets.diskDel),
    path('index/assets/network/', assets.network),
    path('index/assets/network/form_add/', assets.networkForm_add),
    path('index/assets/network/add/', assets.networkAdd),
    url(r'^index/assets/network/form_update/id=(?P<id>\d*)', assets.networkForm_update),
    url(r'^index/assets/network/update/id=(?P<id>\d*)', assets.networkUpdate),
    path('index/assets/network/del/', assets.networkDel),

    # url(r'^', include(router.urls)),

    #    url(r'^serverinfo/', views.serverinfo),
    #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
