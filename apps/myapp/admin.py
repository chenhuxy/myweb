#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin

# Register your models here.
from .models import *



class userGroupAdmin(admin.ModelAdmin):
    list_display = ('name','create_time','update_time',)

class userTypeAdmin(admin.ModelAdmin):
    list_display = ('name','create_time','update_time',)

class userInfoAdmin(admin.ModelAdmin):
    list_display = ('username','password','email','usertype',)
    search_fields = ('username','email',)
    list_filter = ('username','email',)
    #list_display_links = ('username','usertype',)
    #list_editable = ('username','password','email','usertype',)

class wf_infoAdmin(admin.ModelAdmin):
    list_display = ('sponsor','type','content','status','approval','create_time',)
    search_fields = ('sponsor','status','approval',)
    list_filter = ('sponsor','status','approval',)
    list_display_links = ('sponsor',)
    #list_editable = ('content',)

class wf_typeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)

class wf_businessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)

'''
class wf_statusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)
    list_filter = ('status',)
    list_display_links = ('status',)
'''
class act_re_deploymentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class act_ge_bytearrayAdmin(admin.ModelAdmin):
    list_display = ('name',)

class act_hi_actinstAdmin(admin.ModelAdmin):
    list_display = ('act_name',)

class act_hi_attachmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

class act_hi_commentAdmin(admin.ModelAdmin):
    list_display = ('type',)

class act_hi_procinstAdmin(admin.ModelAdmin):
    list_display = ('proc_def_id',)


class act_hi_taskinstAdmin(admin.ModelAdmin):
    list_display = ('task_def_key',)

class act_ru_executionAdmin(admin.ModelAdmin):
    list_display = ('proc_inst_id','act_id',)

class act_ru_taskAdmin(admin.ModelAdmin):
    list_display = ('name','excution_id','parent_task_id',)
######################################################################################################################################

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class AdmininfoAdmin(admin.ModelAdmin):
    list_display = ('username',)
    list_filter = ('username',)
    search_fields = ('username',)

class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class AssetAdmin(admin.ModelAdmin):
    list_display = ('cabinet_num','cabinet_order',)
    list_filter = ('cabinet_num','cabinet_order',)
    search_fields = ('cabinet_num','cabinet_order',)

class ServerAdmin(admin.ModelAdmin):
    list_display = ('hostname','sn','manufactory','model','type','bios',)
    list_filter = ('hostname','sn','manufactory','model','type','bios',)
    search_fields = ('hostname','sn','manufactory','model','type','bios',)

class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('name','sn','manufactory','model',)
    list_filter = ('name','sn','manufactory','model',)
    search_fields = ('name','sn','manufactory','model',)

class CPUAdmin(admin.ModelAdmin):
    list_display = ('name','model','core_num',)
    list_filter = ('name','model','core_num',)
    search_fields = ('name','model','core_num',)

class MemoryAdmin(admin.ModelAdmin):
    list_display = ('slot','model','capacity','ifac_type',)
    list_filter = ('slot','model','capacity','ifac_type',)
    search_fields = ('slot','model','capacity','ifac_type',)

class DiskAdmin(admin.ModelAdmin):
    list_display = ('slot','model','capacity','ifac_type',)
    list_filter = ('slot','model','capacity','ifac_type',)
    search_fields = ('slot','model','capacity','ifac_type',)

class NICAdmin(admin.ModelAdmin):
    list_display = ('name','model','ipaddr','mac',)
    list_filter = ('name','model','ipaddr','mac',)
    search_fields = ('name','model','ipaddr','mac',)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('name','sn','cost','start_date','end_date','license_num',)
    list_filter = ('name','sn','cost','start_date','end_date','license_num',)
    search_fields = ('name','sn','cost','start_date','end_date','license_num',)

class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class IDCAdmin(admin.ModelAdmin):
    list_display = ('region_display_name','display_name','floor',)
    list_filter = ('region_display_name','display_name','floor',)
    search_fields = ('region_display_name','display_name','floor',)

class HandleLogAdmin(admin.ModelAdmin):
    list_display = ('handle_type',)
    list_filter = ('handle_type',)
    search_fields = ('handle_type',)




admin.site.register(userGroup,userGroupAdmin)
admin.site.register(userType,userTypeAdmin)
admin.site.register(userInfo,userInfoAdmin)
admin.site.register(wf_info,wf_infoAdmin)
admin.site.register(wf_type,wf_typeAdmin)
admin.site.register(wf_business,wf_businessAdmin)
#admin.site.register(wf_status,wf_statusAdmin)
admin.site.register(act_re_deployment,act_re_deploymentAdmin)
admin.site.register(act_ge_bytearray,act_ge_bytearrayAdmin)
admin.site.register(act_hi_actinst,act_hi_actinstAdmin)
admin.site.register(act_hi_attachment,act_hi_attachmentAdmin)
admin.site.register(act_hi_comment,act_hi_commentAdmin)
admin.site.register(act_hi_procinst,act_hi_procinstAdmin)
admin.site.register(act_hi_taskinst,act_hi_taskinstAdmin)
admin.site.register(act_ru_execution,act_ru_executionAdmin)
admin.site.register(act_ru_task,act_ru_taskAdmin)



###################################################################################################################################
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Admininfo,AdmininfoAdmin)
admin.site.register(DeviceType,DeviceTypeAdmin)
admin.site.register(DeviceStatus,DeviceStatusAdmin)
admin.site.register(Asset,AssetAdmin)
admin.site.register(Server,ServerAdmin)
admin.site.register(NetworkDevice,NetworkDeviceAdmin)
admin.site.register(CPU,CPUAdmin)
admin.site.register(Memory,MemoryAdmin)
admin.site.register(Disk,DiskAdmin)
admin.site.register(NIC,NICAdmin)
admin.site.register(Contract,ContractAdmin)
admin.site.register(BusinessUnit,BusinessUnitAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(IDC,IDCAdmin)
admin.site.register(HandleLog,HandleLogAdmin)