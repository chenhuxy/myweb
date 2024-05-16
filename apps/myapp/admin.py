#!/usr/bin/env python
# coding:utf-8

from django.contrib import admin

# Register your models here.

from .models import *
# 继承User表，否则admin页面修改密码后明文
from django.contrib.auth.admin import UserAdmin

# admin-log-------------------------------------------------------------------------------------------------------------
"""
用于显示admin内置的django_admin_log表，
content_type指向django_content_type表中的model
"""


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', '__str__',)
    list_display_links = ('action_time',)
    list_filter = ('action_time', 'user', 'content_type',)
    list_per_page = 10
    readonly_fields = (
        'action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message',)


# monitor---------------------------------------------------------------------------------------------------------------

class MonitorPrometheusAdmin(admin.ModelAdmin):
    list_display = ('instance', 'status', 'alertname', 'severity', 'summary', 'description', 'starts_at', 'ends_at',)
    search_fields = ('summary', 'instance', 'description',)
    list_filter = ('alertname', 'severity', 'starts_at', 'ends_at',)
    list_display_links = ('instance',)
    list_per_page = 10


class MonitorSkywalkingAdmin(admin.ModelAdmin):
    list_display = ('scope', 'name', 'ruleName', 'alarmMessage', 'startTime',)
    search_fields = ('ruleName', 'alarmMessage',)
    list_filter = ('scope', 'name', 'startTime')
    list_display_links = ('name',)
    list_per_page = 10


admin.site.register(MonitorPrometheus, MonitorPrometheusAdmin)
admin.site.register(MonitorSkywalking, MonitorSkywalkingAdmin)


# task-deploy-----------------------------------------------------------------------------------------------------------

class deploy_script_typeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 10


class deploy_appAdmin(admin.ModelAdmin):
    list_display = ('proj_name', 'proj_id', 'unit', 'update_time',)
    search_fields = ('proj_name',)
    list_filter = ('proj_name', 'unit',)
    list_display_links = ('proj_name',)
    list_per_page = 10


class deploy_list_detailAdmin(admin.ModelAdmin):
    list_display = ('proj_name', 'proj_id', 'tag', 'status', 'unit', 'update_time',)
    search_fields = ('proj_name', 'tag',)
    list_filter = ('proj_name', 'status', 'unit',)
    list_display_links = ('proj_name',)
    list_per_page = 10


# admin.site.register(business,businessAdmin)
admin.site.register(deploy_script_type, deploy_script_typeAdmin)
admin.site.register(deploy_app, deploy_appAdmin)
admin.site.register(deploy_list_detail, deploy_list_detailAdmin)


# users-----------------------------------------------------------------------------------------------------------------

class userInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    # list_display_links = ('username','usertype',)
    # list_editable = ('username','password','email','usertype',)
    # exclude = ('password',)##隐藏某个字段
    list_per_page = 10


'''
class userGroupAdmin(admin.ModelAdmin):
    list_display = ('name','create_time','update_time',)


class userTypeAdmin(admin.ModelAdmin):
    list_display = ('name','create_time','update_time',)
'''
# 继承User表，否则admin页面修改密码后明文
admin.site.register(userInfo, UserAdmin)


# admin.site.register(userGroup,userGroupAdmin)
# admin.site.register(userType,userTypeAdmin)

# workflow--------------------------------------------------------------------------------------------------------------

class wf_infoAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'type', 'content', 'status', 'create_time', 'memo',)
    search_fields = ('content', 'memo',)
    list_filter = ('sponsor', 'status', 'type',)
    list_display_links = ('sponsor',)
    # list_editable = ('content',)
    list_per_page = 10


class wf_info_process_historyAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'type', 'content', 'status', 'create_time', 'memo',)
    search_fields = ('content', 'memo',)
    list_filter = ('sponsor', 'status', 'type',)
    list_display_links = ('sponsor',)
    # list_editable = ('content',)
    list_per_page = 10


class wf_typeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


class wf_businessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


admin.site.register(wf_info, wf_infoAdmin)
admin.site.register(wf_info_process_history, wf_info_process_historyAdmin)
admin.site.register(wf_type, wf_typeAdmin)
admin.site.register(wf_business, wf_businessAdmin)


# assets----------------------------------------------------------------------------------------------------------------


class AssetDeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetDeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetAdmin(admin.ModelAdmin):
    list_display = ('ip', 'hostname', 'env_type', 'device_type', 'os_type', 'business_unit', 'admin', 'username',
                    'password')
    list_filter = ('env_type', 'device_type', 'os_type', 'business_unit', 'admin', 'is_docker')
    search_fields = ('ip', 'memo', 'hostname', 'sn',)
    list_per_page = 10


class AssetEnvTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetOsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetIDCAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'floor', 'region_display_name',)
    list_filter = ('display_name', 'floor', 'region_display_name',)
    search_fields = ('display_name', 'floor', 'region_display_name',)
    list_per_page = 10


admin.site.register(AssetDeviceType, AssetDeviceTypeAdmin)
admin.site.register(AssetDeviceStatus, AssetDeviceStatusAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetEnvType, AssetEnvTypeAdmin)
admin.site.register(AssetOsType, AssetOsTypeAdmin)
admin.site.register(AssetTag, AssetTagAdmin)
admin.site.register(AssetIDC, AssetIDCAdmin)
