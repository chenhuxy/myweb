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
    list_display = ('action_time', 'user', 'content_type', '__str__')
    list_display_links = ('action_time',)
    list_filter = ('action_time', 'user', 'content_type')
    list_per_page = 10
    readonly_fields = (
        'action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')


'''
# monitor---------------------------------------------------------------------------------------------------------------

class monitorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(monitor, monitorAdmin)
'''


# task-deploy-----------------------------------------------------------------------------------------------------------

class deploy_script_typeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10


class deploy_appAdmin(admin.ModelAdmin):
    list_display = ('proj_name', 'proj_id', 'unit', 'update_time', 'action',)
    search_fields = ('proj_name', 'unit')
    list_filter = ('proj_name', 'unit')
    list_display_links = ('proj_name',)
    list_per_page = 10


class deploy_list_detailAdmin(admin.ModelAdmin):
    list_display = ('proj_name', 'proj_id', 'unit', 'update_time', 'action', 'tag', 'status', 'task_id', 'task_log')
    search_fields = ('proj_name', 'tag', 'status')
    list_filter = ('proj_name', 'tag', 'status')
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
    list_display = ('sponsor', 'type', 'content', 'status', 'create_time',)
    search_fields = ('sponsor', 'status',)
    list_filter = ('sponsor', 'status',)
    list_display_links = ('sponsor',)
    # list_editable = ('content',)
    list_per_page = 10


class wf_info_process_historyAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'type', 'content', 'status', 'create_time',)
    search_fields = ('sponsor', 'status',)
    list_filter = ('sponsor', 'status',)
    list_display_links = ('sponsor',)
    # list_editable = ('content',)
    list_per_page = 10


class wf_typeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


class businessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


admin.site.register(wf_info, wf_infoAdmin)
admin.site.register(wf_info_process_history, wf_info_process_historyAdmin)
admin.site.register(wf_type, wf_typeAdmin)

# assets----------------------------------------------------------------------------------------------------------------
'''
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
'''
'''
class AdmininfoAdmin(admin.ModelAdmin):
    list_display = ('username',)
    list_filter = ('username',)
    search_fields = ('username',)
'''


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class AssetAdmin(admin.ModelAdmin):
    list_display = ('cabinet_num', 'cabinet_order',)
    list_filter = ('cabinet_num', 'cabinet_order',)
    search_fields = ('cabinet_num', 'cabinet_order',)
    list_per_page = 10


class ServerAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'sn', 'manufactory', 'model', 'type', 'bios',)
    list_filter = ('hostname', 'sn', 'manufactory', 'model', 'type', 'bios',)
    search_fields = ('hostname', 'sn', 'manufactory', 'model', 'type', 'bios',)
    list_per_page = 10


class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'sn', 'manufactory', 'model',)
    list_filter = ('name', 'sn', 'manufactory', 'model',)
    search_fields = ('name', 'sn', 'manufactory', 'model',)
    list_per_page = 10


class CPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'core_num',)
    list_filter = ('name', 'model', 'core_num',)
    search_fields = ('name', 'model', 'core_num',)
    list_per_page = 10


class MemoryAdmin(admin.ModelAdmin):
    list_display = ('slot', 'model', 'capacity', 'ifac_type',)
    list_filter = ('slot', 'model', 'capacity', 'ifac_type',)
    search_fields = ('slot', 'model', 'capacity', 'ifac_type',)
    list_per_page = 10


class DiskAdmin(admin.ModelAdmin):
    list_display = ('slot', 'model', 'capacity', 'ifac_type',)
    list_filter = ('slot', 'model', 'capacity', 'ifac_type',)
    search_fields = ('slot', 'model', 'capacity', 'ifac_type',)
    list_per_page = 10


class NICAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'ipaddr', 'mac',)
    list_filter = ('name', 'model', 'ipaddr', 'mac',)
    search_fields = ('name', 'model', 'ipaddr', 'mac',)
    list_per_page = 10


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'sn', 'cost', 'start_date', 'end_date', 'license_num',)
    list_filter = ('name', 'sn', 'cost', 'start_date', 'end_date', 'license_num',)
    search_fields = ('name', 'sn', 'cost', 'start_date', 'end_date', 'license_num',)
    list_per_page = 10


'''
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
'''


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10


class IDCAdmin(admin.ModelAdmin):
    list_display = ('region_display_name', 'display_name', 'floor',)
    list_filter = ('region_display_name', 'display_name', 'floor',)
    search_fields = ('region_display_name', 'display_name', 'floor',)
    list_per_page = 10


class HandleLogAdmin(admin.ModelAdmin):
    list_display = ('handle_type',)
    list_filter = ('handle_type',)
    search_fields = ('handle_type',)
    list_per_page = 10


# admin.site.register(UserProfile,UserProfileAdmin)
# admin.site.register(Admininfo,AdmininfoAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(DeviceStatus, DeviceStatusAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(NetworkDevice, NetworkDeviceAdmin)
admin.site.register(CPU, CPUAdmin)
admin.site.register(Memory, MemoryAdmin)
admin.site.register(Disk, DiskAdmin)
admin.site.register(NIC, NICAdmin)
admin.site.register(Contract, ContractAdmin)
# admin.site.register(BusinessUnit,BusinessUnitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IDC, IDCAdmin)
admin.site.register(HandleLog, HandleLogAdmin)
