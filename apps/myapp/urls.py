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
    url(r'^login/forget_pass/send/', account.forget_pass_send, ),
    path('login/forget_pass/change/', account.forget_pass_change, ),

    # permission--------------------------------------------------------------------------------------------------------

    url(r'index/permission/list/(?P<page>\d*)', account.permission, ),

    # users-------------------------------------------------------------------------------------------------------------

    path('index/table/usergroup/list/', account.usergroup, ),
    path('index/table/user/form_add/', account.user_form_add, ),
    path('index/table/usergroup/form_add/', account.usergroup_form_add, ),
    # path('index/table/user/form_update/',account.userForm_update),
    url(r'^index/table/user/form_update/userid=(?P<userid>\d*)', account.user_form_update, ),
    url(r'^index/table/user/form_change_password/username=(?P<username>\w+)', account.user_form_change_password, ),
    url(r'^index/table/user/form_get_profile/username=(?P<username>\w+)', account.user_form_get_profile, ),
    url(r'^index/table/usergroup/form_update/id=(?P<id>\d*)', account.usergroup_form_update, ),
    path('index/table/user/add/', account.user_add, ),
    path('index/table/usergroup/add/', account.usergroup_add, ),
    url(r'^index/table/user/update/userid=(?P<userid>\d*)', account.user_update, ),
    url(r'^index/table/user/show_detail/userid=(?P<userid>\d*)', account.user_detail, ),
    url(r'^index/table/user/change_password/username=(?P<username>\w+)', account.user_change_password, ),
    url(r'^index/table/usergroup/update/id=(?P<id>\d*)', account.usergroup_update, ),
    url(r'^index/table/usergroup/show_detail/id=(?P<id>\d*)', account.usergroup_detail, ),
    path('index/table/user/del/', account.user_del, ),
    path('index/table/user/resetPwd/', account.reset_password, ),
    path('index/table/usergroup/del/', account.usergroup_del, ),
    url(r'^index/table/user/search/', account.user_search, ),
    url(r'^index/table/user/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)', account.user_search_result, ),
    url(r'^index/table/user/list/(?P<page>\d*)', account.user, ),

    # monitor-----------------------------------------------------------------------------------------------------------

    path('index/monitor/zabbix/alert/list/', zabbix.zabbix_trigger, ),
    path('index/monitor/skywalking/alert/send/', skywalking.send_alert, ),
    path('index/monitor/skywalking/dashboard/', skywalking.dashboard, ),
    url(r'^index/monitor/skywalking/alert/list/(?P<page>\d*)', skywalking.skywalking_alert, ),
    path('index/monitor/prometheus/alert/send/', prometheus.send_alert, ),
    path('index/monitor/gitlab/', gitlab_helper.git_project, ),
    url(r'^index/monitor/prometheus/alert/list/(?P<page>\d*)', prometheus.prometheus_alert, ),
    path('index/monitor/prometheus/dashboard/', prometheus.dashboard, ),
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
    path('index/wf/wftype/del/', workflow.wftype_del, ),
    path('index/wf/wftype/change/', workflow.wftype_change, ),
    path('index/wf/proj/search/', workflow.wf_proj_search, ),
    # path('index/wf/wftype/change2/', workflow.wftypeChange2, ),
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
    path('index/deploy/ansible-vars/list/', deploy.ansible_vars),
    path('index/deploy/ansible-vars/form-add/', deploy.ansible_vars_form_add),
    path('index/deploy/ansible-vars/add/', deploy.ansible_vars_add),
    url(r'^index/deploy/ansible-vars/form-update/id=(?P<id>\d*)', deploy.ansible_vars_form_update),
    url(r'^index/deploy/ansible-vars/update/id=(?P<id>\d*)', deploy.ansible_vars_update),
    path('index/deploy/ansible-vars/del/', deploy.ansible_vars_del),

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

    path('index/assets/env-type/list/', assets.env_type),
    path('index/assets/env-type/form-add/', assets.env_type_form_add),
    path('index/assets/env-type/add/', assets.env_type_add),
    url(r'^index/assets/env-type/form-update/id=(?P<id>\d*)', assets.env_type_form_update),
    url(r'^index/assets/env-type/update/id=(?P<id>\d*)', assets.env_type_update),
    path('index/assets/env-type/del/', assets.env_type_del),
    path('index/assets/os-type/list/', assets.os_type),
    path('index/assets/os-type/form-add/', assets.os_type_form_add),
    path('index/assets/os-type/add/', assets.os_type_add),
    url(r'^index/assets/os-type/form-update/id=(?P<id>\d*)', assets.os_type_form_update),
    url(r'^index/assets/os-type/update/id=(?P<id>\d*)', assets.os_type_update),
    path('index/assets/os-type/del/', assets.os_type_del),
    path('index/assets/device-type/list/', assets.device_type),
    path('index/assets/device-type/form-add/', assets.device_type_form_add),
    path('index/assets/device-type/add/', assets.device_type_add),
    url(r'^index/assets/device-type/form-update/id=(?P<id>\d*)', assets.device_type_form_update),
    url(r'^index/assets/device-type/update/id=(?P<id>\d*)', assets.device_type_update),
    path('index/assets/device-type/del/', assets.device_type_del),
    path('index/assets/device-status/list/', assets.device_status),
    path('index/assets/device-status/form-add/', assets.device_status_form_add),
    path('index/assets/device-status/add/', assets.device_status_add),
    url(r'^index/assets/device-status/form-update/id=(?P<id>\d*)', assets.device_status_form_update),
    url(r'^index/assets/device-status/update/id=(?P<id>\d*)', assets.device_status_update),
    path('index/assets/device-status/del/', assets.device_status_del),
    path('index/assets/idc/list/', assets.idc),
    path('index/assets/idc/form-add/', assets.idc_form_add),
    path('index/assets/idc/add/', assets.idc_add),
    url(r'^index/assets/idc/form-update/id=(?P<id>\d*)', assets.idc_form_update),
    url(r'^index/assets/idc/update/id=(?P<id>\d*)', assets.idc_update),
    path('index/assets/idc/del/', assets.idc_del),
    path('index/assets/tag/list/', assets.tag),
    path('index/assets/tag/form-add/', assets.tag_form_add),
    path('index/assets/tag/add/', assets.tag_add),
    url(r'^index/assets/tag/form-update/id=(?P<id>\d*)', assets.tag_form_update),
    url(r'^index/assets/tag/update/id=(?P<id>\d*)', assets.tag_update),
    path('index/assets/tag/del/', assets.tag_del),
    url(r'index/assets/asset/list/(?P<page>\d*)', assets.asset),
    url(r'^index/assets/asset/show-detail/id=(?P<id>\d*)', assets.asset_detail, ),
    path('index/assets/asset/form-add/', assets.asset_form_add),
    path('index/assets/asset/add/', assets.asset_add),
    path('index/assets/asset/upload/', assets.asset_upload),
    path('index/assets/asset/export-all/', assets.asset_export),
    url(r'^index/assets/asset/form-update/id=(?P<id>\d*)', assets.asset_form_update),
    url(r'^index/assets/asset/update/id=(?P<id>\d*)', assets.asset_update),
    path('index/assets/asset/del/', assets.asset_del),
    url(r'^index/assets/asset/search/', assets.asset_search, ),
    url(r'^index/assets/asset/search_result/keyword=(?P<keyword>[0-9.]+)&page=(?P<page>\d+)',
        assets.asset_search_result, ),
    url(r'^index/assets/asset/search_result/keyword=(?P<keyword>\w+)&page=(?P<page>\d+)',
        assets.asset_search_result, ),

    # url(r'^', include(router.urls)),

    #    url(r'^serverinfo/', views.serverinfo),
    #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
