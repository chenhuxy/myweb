#!/usr/bin/env python
# coding:utf-8

from django.db import models

# Create your models here

from django.contrib.auth.models import AbstractUser


# OpLogs----------------------------------------------------------------------------------------------------------------
class OpLogs(models.Model):
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='请求用户')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=32, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    rp_status_code = models.IntegerField(verbose_name='状态码')
    rp_duration = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'op_logs'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.re_user


# users-----------------------------------------------------------------------------------------------------------------

'''
class userType(models.Model):
    name = models.CharField('用户类型',max_length=200,default='user')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
'''

'''
class userGroup(models.Model):
    name = models.CharField('所属组',max_length=200,default='default')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
       verbose_name = '用户组'
       verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
'''


class userInfo(AbstractUser):
    workflow_order = models.IntegerField('工作流编号', default=0, )
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


'''
class userInfo(models.Model):
    username = models.CharField('用户名',max_length=200)
    email = models.EmailField('邮箱')
    password = models.CharField('密码',max_length=100)
    usertype = models.ForeignKey(userType,verbose_name='用户类型',on_delete=models.CASCADE)
    #STATUS_CHOICE = (
    #    ('0', '否'),
    #    ('1', '是'),
    #)
    is_active = models.BooleanField('激活',max_length=200,default=True,)
    group = models.ManyToManyField(userGroup,verbose_name='用户组',blank=True,)
    workflow_order = models.IntegerField('工作流编号',default=0,)
    #ROLE_CHOICE = (
    #    ('0', '否'),
    #    ('1', '是'),
    #)
    #approval = models.CharField('是否部门主管',max_length=128,choices=ROLE_CHOICE,default='0')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    memo = models.TextField('备注', blank=True, null=True)
    class Meta:
        verbose_name = '登录用户'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.username,self.usertype
'''

'''
class UserProfile(models.Model):
    name = models.CharField('名字',max_length=256)
    email = models.EmailField('邮箱',max_length=256)
    mobile = models.CharField('手机',max_length=256)
    memo = models.TextField('备注',blank=True,null=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)
    class Meta:
        verbose_name = '管理用户信息'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
'''

'''
class Admininfo(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    username = models.CharField('用户名',max_length=256)
    password = models.CharField('密码',max_length=256)
    class Meta:
        verbose_name = '管理用户'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.username
'''

'''
# monitor---------------------------------------------------------------------------------------------------------------

class monitor(models.Model):
    name = models.CharField('名称', max_length=256)

    class Meta:
        verbose_name = '监控权限'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
'''


# task-deploy-----------------------------------------------------------------------------------------------------------

class deploy_script_type(models.Model):
    name = models.CharField('脚本类型', max_length=200, default='shell', )

    class Meta:
        verbose_name = '脚本类型'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class deploy_app(models.Model):
    unit = models.ForeignKey('wf_business', on_delete=models.CASCADE, verbose_name='业务单元', related_name='unit', )
    proj_name = models.CharField('项目名称', max_length=128, )
    proj_id = models.CharField('项目id', max_length=128, )
    update_time = models.DateTimeField('修改时间', auto_now=True)
    action = models.CharField('动作', max_length=128)

    class Meta:
        verbose_name = '应用列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.proj_name


class deploy_list_detail(models.Model):
    unit = models.CharField('业务单元', max_length=128)
    proj_name = models.CharField('项目名称', max_length=128)
    proj_id = models.CharField('项目id', max_length=128, )
    tag = models.CharField('发布tag', max_length=128)
    task_id = models.CharField('任务id', max_length=128, )
    task_log = models.TextField('任务日志', blank=True, null=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('任务状态', max_length=128)
    action = models.CharField('动作', max_length=128)

    class Meta:
        verbose_name = '发布列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.proj_name


'''
class business(models.Model):
    name = models.CharField('业务单元', max_length=128,  )
    admin = models.ForeignKey('userInfo',on_delete=models.CASCADE,verbose_name='业务管理员',related_name='unit_admin',)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
        verbose_name = '业务单元'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
'''


# workflow--------------------------------------------------------------------------------------------------------------

class wf_business(models.Model):
    name = models.CharField('业务单元', max_length=128, default='default', )
    # proj_id = models.CharField('项目id',max_length=128,)
    # repo = models.CharField('项目地址',max_length=128,)
    admin = models.ForeignKey('userInfo', on_delete=models.CASCADE, verbose_name='业务负责人', related_name='admin', )
    approval = models.ManyToManyField('userInfo', verbose_name='审批人', blank=True, related_name='approval', )
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '业务单元'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class wf_type(models.Model):
    name = models.CharField('请求类型', max_length=128, default='生产发布', )
    # 2023/08/15
    # deploy = models.ForeignKey(deploy_list,verbose_name='发布服务',on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '工单类型'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class wf_info(models.Model):
    sn = models.CharField('请求编号', max_length=128, )
    title = models.CharField('标题', max_length=256, )
    sponsor = models.CharField('发起人', max_length=128, )
    type = models.ForeignKey(wf_type, verbose_name='请求类型', on_delete=models.CASCADE)
    content = models.TextField('请求内容', blank=True, null=True)
    status = models.CharField('工单状态', max_length=128, default='未提交')
    business = models.ForeignKey('wf_business', on_delete=models.CASCADE)
    flow_id = models.IntegerField('流程id', default=-1)
    assignee = models.CharField('当前处理人', max_length=128, )
    next_assignee = models.CharField('下个处理人', max_length=128, )
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    finish_time = models.DateTimeField('完成时间', auto_now=True)
    # duration = models.BigIntegerField('耗时')
    memo = models.TextField('备注', blank=True, null=True)
    # 2023/08/16
    proj_name = models.CharField('项目名称', max_length=128, blank=True, null=True)
    proj_tag = models.CharField('项目tag', max_length=128, blank=True, null=True)
    # 2023/08/17
    proj_id = models.CharField('项目id', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = '工单流程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.type, self.status


class wf_info_process_history(models.Model):
    sn = models.CharField('请求编号', max_length=128, )
    title = models.CharField('标题', max_length=256, )
    sponsor = models.CharField('发起人', max_length=128, )
    type = models.ForeignKey(wf_type, verbose_name='请求类型', on_delete=models.CASCADE)
    content = models.TextField('请求内容', blank=True, null=True)
    status = models.CharField('工单状态', max_length=128, default='处理中')
    business = models.ForeignKey('wf_business', on_delete=models.CASCADE)
    flow_id = models.IntegerField('流程id', )
    assignee = models.CharField('当前处理人', max_length=128, )
    next_assignee = models.CharField('下个处理人', max_length=128, )
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    finish_time = models.DateTimeField('完成时间', auto_now=True)
    # duration = models.BigIntegerField('耗时')
    memo = models.TextField('备注', blank=True, null=True)
    suggest = models.CharField('审批结果', max_length=128, blank=True, null=True)
    suggest_content = models.TextField('审批意见', blank=True, null=True)
    # 2023/08/16
    proj_name = models.CharField('项目名称', max_length=128, blank=True, null=True)
    proj_tag = models.CharField('项目tag', max_length=128, blank=True, null=True)
    # 2023/08/17
    proj_id = models.CharField('项目id', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = '工单流程历史'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.type, self.status


# assets----------------------------------------------------------------------------------------------------------------

'''
class UserProfile(models.Model):
    name = models.CharField('名字',max_length=256)
    email = models.EmailField('邮箱',max_length=256)
    mobile = models.CharField('手机',max_length=256)
    memo = models.TextField('备注',blank=True,null=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)
    class Meta:
        verbose_name = '管理用户信息'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Admininfo(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    username = models.CharField('用户名',max_length=256)
    password = models.CharField('密码',max_length=256)
    class Meta:
        verbose_name = '管理用户'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.username
'''


class DeviceStatus(models.Model):
    name = models.CharField('名字', max_length=256, default='未上线')
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '设备状态'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class DeviceType(models.Model):
    name = models.CharField('名称', max_length=256)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '设备类型'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Asset(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    device_status = models.ForeignKey(DeviceStatus, on_delete=models.CASCADE)
    cabinet_num = models.CharField('机柜号', max_length=256, blank=True, null=True)
    cabinet_order = models.CharField('机架号', max_length=256, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True, null=True)
    idc = models.ForeignKey('IDC', verbose_name='idc机房', blank=True, null=True, on_delete=models.CASCADE)
    business_unit = models.ForeignKey('wf_business', verbose_name='所属业务线', blank=True, null=True,
                                      on_delete=models.CASCADE, related_name='business_unit', )
    admin = models.ForeignKey('userInfo', verbose_name='设备管理员', blank=True, null=True, related_name='+',
                              on_delete=models.CASCADE)
    contract = models.ForeignKey('Contract', verbose_name='合同', blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'type:%s %s:%s' % (self.device_type, self.cabinet_num, self.cabinet_order)


class Server(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    hostname = models.CharField('主机名', max_length=128, blank=True, unique=True)
    ip = models.GenericIPAddressField('ip地址', unique=True, )
    sn = models.CharField('SN号', max_length=256)
    manufactory = models.CharField('厂商', max_length=256, blank=True, null=True)
    model = models.CharField('型号', max_length=256, blank=True, null=True)
    bios = models.CharField('BIOS', max_length=256, blank=True, null=True)
    type = models.CharField('虚拟机', max_length=256, )
    memo = models.TextField('备注', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '服务器信息'
        verbose_name_plural = verbose_name
        index_together = ['sn', 'asset']

    def __unicode__(self):
        return self.sn


class NetworkDevice(models.Model):
    name = models.CharField('设备名称', max_length=256, blank=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=256)
    manufactory = models.CharField('厂商', max_length=256, blank=True, null=True)
    model = models.CharField('型号', max_length=256, blank=True, null=True)
    memo = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)

    class Meta:
        verbose_name = '网络设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s:%s' % (self.name, self.sn)


class CPU(models.Model):
    name = models.CharField('CPU名称', max_length=256, blank=True)
    model = models.CharField('CPU型号', max_length=256, blank=True)
    core_num = models.IntegerField('CPU核数', blank=True, default=1)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)
    server_info = models.ForeignKey(Server, on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = 'CPU信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s:%s' % (self.name, self.model)


class Memory(models.Model):
    slot = models.CharField('插槽名称', max_length=256, blank=True)
    model = models.CharField('内存型号', max_length=256, blank=True)
    capacity = models.FloatField('内存容量', blank=True)
    ifac_type = models.CharField('接口类型', max_length=256, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)
    server_info = models.ForeignKey(Server, on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '内存信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s:%s' % (self.slot, self.capacity)


class Disk(models.Model):
    slot = models.CharField('插槽名称', max_length=256, blank=True)
    model = models.CharField('磁盘型号', max_length=256, blank=True)
    capacity = models.FloatField('磁盘容量', blank=True)
    ifac_type = models.CharField('接口类型', max_length=256, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)
    server_info = models.ForeignKey(Server, on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '磁盘信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s:%s' % (self.slot, self.capacity)


class NIC(models.Model):
    name = models.CharField('网卡名称', max_length=256, blank=True)
    model = models.CharField('网卡型号', max_length=256, blank=True)
    ipaddr = models.GenericIPAddressField('ip地址')
    mac = models.CharField('MAC地址', max_length=256)
    netmask = models.CharField('子网掩码', max_length=256, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)
    server_info = models.ForeignKey(Server, on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '网卡信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s:%s' % (self.name, self.ipaddr)


class Contract(models.Model):
    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=256)
    cost = models.IntegerField('合同金额')
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    license_num = models.IntegerField('license数量', blank=True)
    memo = models.TextField('备注', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, blank=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


'''
class BusinessUnit(models.Model):
    name = models.CharField('业务线',max_length=128,unique=True)
    contact = models.ForeignKey('UserProfile',default=None,on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
'''


class Tag(models.Model):
    name = models.CharField('标签名', max_length=256)
    memo = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class IDC(models.Model):
    region_display_name = models.CharField('区域名称', max_length=256, default=None)
    display_name = models.CharField('机房名称', max_length=256, default=None)
    floor = models.IntegerField('楼层', default=1)
    memo = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'region:%s idc:%s floor:%s' % (self.region_display_name, self.display_name, self.floor)


class HandleLog(models.Model):
    handle_type = models.CharField('操作类型', max_length=256)
    summary = models.CharField(max_length=256)
    detail = models.TextField()
    creater = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    memo = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.handle_type
