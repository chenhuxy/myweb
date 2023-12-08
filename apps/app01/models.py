#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.db import models


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()


class UserProfile(models.Model):
    name = models.CharField('名字', max_length=256)
    email = models.EmailField('邮箱', max_length=256)
    mobile = models.CharField('手机', max_length=256)
    memo = models.TextField('备注', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Admininfo(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    username = models.CharField('用户名', max_length=256)
    password = models.CharField('密码', max_length=256)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


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
    idc = models.ForeignKey('CmdbIDC', verbose_name='idc机房', blank=True, null=True, on_delete=models.CASCADE)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='所属业务线', blank=True, null=True,
                                      on_delete=models.CASCADE)
    admin = models.ForeignKey('UserProfile', verbose_name='设备管理员', blank=True, null=True, related_name='+',
                              on_delete=models.CASCADE)
    contract = models.ForeignKey('CmdbContract', verbose_name='合同', blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField('CmdbTag', verbose_name='标签', blank=True)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'type:%s %s:%s' % (self.device_type, self.cabinet_num, self.cabinet_order)


class Server(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    hostname = models.CharField('主机名', max_length=128, blank=True, unique=True)
    sn = models.CharField('SN号', max_length=256)
    manufactory = models.CharField('厂商', max_length=256, blank=True, null=True)
    model = models.CharField('型号', max_length=256, blank=True, null=True)
    bios = models.CharField('BIOS', max_length=256, blank=True, null=True)
    type = models.BooleanField('虚拟机', default=False)
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
    netmask = models.CharField(max_length=256, blank=True)
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


class BusinessUnit(models.Model):
    name = models.CharField('业务线', max_length=128, unique=True)
    contact = models.ForeignKey('UserProfile', default=None, on_delete=models.CASCADE)
    memo = models.TextField('备注', blank=True, null=True)

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


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
    creater = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, blank=True)
    memo = models.TextField('备注', blank=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.handle_type
