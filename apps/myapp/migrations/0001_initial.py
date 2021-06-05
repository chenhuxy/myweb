# Generated by Django 2.1.7 on 2021-06-05 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admininfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
            ],
            options={
                'verbose_name': '管理用户',
                'verbose_name_plural': '管理用户',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabinet_num', models.CharField(blank=True, max_length=256, null=True, verbose_name='机柜号')),
                ('cabinet_order', models.CharField(blank=True, max_length=256, null=True, verbose_name='机架号')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '资产总表',
                'verbose_name_plural': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='合同号')),
                ('name', models.CharField(max_length=256, verbose_name='合同名称')),
                ('cost', models.IntegerField(verbose_name='合同金额')),
                ('start_date', models.DateTimeField(blank=True)),
                ('end_date', models.DateTimeField(blank=True)),
                ('license_num', models.IntegerField(blank=True, verbose_name='license数量')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '合同',
                'verbose_name_plural': '合同',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='CPU名称')),
                ('model', models.CharField(blank=True, max_length=256, verbose_name='CPU型号')),
                ('core_num', models.IntegerField(blank=True, default=1, verbose_name='CPU核数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': 'CPU信息',
                'verbose_name_plural': 'CPU信息',
            },
        ),
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='未上线', max_length=256, verbose_name='名字')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '设备状态',
                'verbose_name_plural': '设备状态',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '设备类型',
                'verbose_name_plural': '设备类型',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(blank=True, max_length=256, verbose_name='插槽名称')),
                ('model', models.CharField(blank=True, max_length=256, verbose_name='磁盘型号')),
                ('capacity', models.FloatField(blank=True, verbose_name='磁盘容量')),
                ('ifac_type', models.CharField(blank=True, max_length=256, verbose_name='接口类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '磁盘信息',
                'verbose_name_plural': '磁盘信息',
            },
        ),
        migrations.CreateModel(
            name='HandleLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle_type', models.CharField(max_length=256, verbose_name='操作类型')),
                ('summary', models.CharField(max_length=256)),
                ('detail', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_display_name', models.CharField(default=None, max_length=256, verbose_name='区域名称')),
                ('display_name', models.CharField(default=None, max_length=256, verbose_name='机房名称')),
                ('floor', models.IntegerField(default=1, verbose_name='楼层')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(blank=True, max_length=256, verbose_name='插槽名称')),
                ('model', models.CharField(blank=True, max_length=256, verbose_name='内存型号')),
                ('capacity', models.FloatField(blank=True, verbose_name='内存容量')),
                ('ifac_type', models.CharField(blank=True, max_length=256, verbose_name='接口类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '内存信息',
                'verbose_name_plural': '内存信息',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='设备名称')),
                ('sn', models.CharField(max_length=256, verbose_name='SN号')),
                ('manufactory', models.CharField(blank=True, max_length=256, null=True, verbose_name='厂商')),
                ('model', models.CharField(blank=True, max_length=256, null=True, verbose_name='型号')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Asset')),
            ],
            options={
                'verbose_name': '网络设备信息',
                'verbose_name_plural': '网络设备信息',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='网卡名称')),
                ('model', models.CharField(blank=True, max_length=256, verbose_name='网卡型号')),
                ('ipaddr', models.GenericIPAddressField(verbose_name='ip地址')),
                ('mac', models.CharField(max_length=256, verbose_name='MAC地址')),
                ('netmask', models.CharField(blank=True, max_length=256, verbose_name='子网掩码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '网卡信息',
                'verbose_name_plural': '网卡信息',
            },
        ),
        migrations.CreateModel(
            name='scriptType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='shell', max_length=200, verbose_name='脚本类型')),
            ],
            options={
                'verbose_name': '脚本类型',
                'verbose_name_plural': '脚本类型',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(blank=True, max_length=128, unique=True, verbose_name='主机名')),
                ('sn', models.CharField(max_length=256, verbose_name='SN号')),
                ('manufactory', models.CharField(blank=True, max_length=256, null=True, verbose_name='厂商')),
                ('model', models.CharField(blank=True, max_length=256, null=True, verbose_name='型号')),
                ('bios', models.CharField(blank=True, max_length=256, null=True, verbose_name='BIOS')),
                ('type', models.BooleanField(default=False, verbose_name='虚拟机')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Asset')),
            ],
            options={
                'verbose_name': '服务器信息',
                'verbose_name_plural': '服务器信息',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='标签名')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='userGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=200, verbose_name='所属组')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
            },
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('is_active', models.BooleanField(default=True, max_length=200, verbose_name='激活')),
                ('workflow_order', models.IntegerField(default=0, verbose_name='工作流编号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('group', models.ManyToManyField(blank=True, to='myapp.userGroup', verbose_name='用户组')),
            ],
            options={
                'verbose_name': '登录用户',
                'verbose_name_plural': '登录用户',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='名字')),
                ('email', models.EmailField(max_length=256, verbose_name='邮箱')),
                ('mobile', models.CharField(max_length=256, verbose_name='手机')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '管理用户信息',
                'verbose_name_plural': '管理用户信息',
            },
        ),
        migrations.CreateModel(
            name='userType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='user', max_length=200, verbose_name='用户类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户类型',
                'verbose_name_plural': '用户类型',
            },
        ),
        migrations.CreateModel(
            name='wf_business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=128, verbose_name='业务单元')),
                ('proj_id', models.CharField(default=183, max_length=128, verbose_name='项目id')),
                ('repo', models.CharField(max_length=128, verbose_name='项目地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='myapp.userInfo', verbose_name='业务管理员')),
                ('approval', models.ManyToManyField(blank=True, related_name='approval', to='myapp.userInfo', verbose_name='审批人')),
            ],
            options={
                'verbose_name': '业务单元',
                'verbose_name_plural': '业务单元',
            },
        ),
        migrations.CreateModel(
            name='wf_business_deploy_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=128, verbose_name='业务单元')),
                ('proj_id', models.CharField(default=183, max_length=128, verbose_name='项目id')),
                ('repo', models.CharField(max_length=128, verbose_name='项目地址')),
                ('branch', models.CharField(max_length=128, verbose_name='项目分支')),
                ('tag', models.CharField(max_length=128, verbose_name='项目tag')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='发布时间')),
                ('state', models.CharField(max_length=128, verbose_name='发布状态')),
                ('logs', models.TextField(blank=True, null=True, verbose_name='发布日志')),
                ('opertator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userInfo')),
            ],
            options={
                'verbose_name': '发布历史',
                'verbose_name_plural': '发布历史',
            },
        ),
        migrations.CreateModel(
            name='wf_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, verbose_name='请求编号')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('sponsor', models.CharField(max_length=128, verbose_name='发起人')),
                ('content', models.TextField(blank=True, null=True, verbose_name='请求内容')),
                ('status', models.CharField(default='未提交', max_length=128, verbose_name='工单状态')),
                ('flow_id', models.IntegerField(default=-1, verbose_name='流程id')),
                ('assignee', models.CharField(max_length=128, verbose_name='当前处理人')),
                ('next_assignee', models.CharField(max_length=128, verbose_name='下个处理人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('finish_time', models.DateTimeField(auto_now=True, verbose_name='完成时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.wf_business')),
            ],
            options={
                'verbose_name': '工单流程',
                'verbose_name_plural': '工单流程',
            },
        ),
        migrations.CreateModel(
            name='wf_info_history_process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, verbose_name='请求编号')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('sponsor', models.CharField(max_length=128, verbose_name='发起人')),
                ('content', models.TextField(blank=True, null=True, verbose_name='请求内容')),
                ('status', models.CharField(default='处理中', max_length=128, verbose_name='工单状态')),
                ('flow_id', models.IntegerField(verbose_name='流程id')),
                ('assignee', models.CharField(max_length=128, verbose_name='当前处理人')),
                ('next_assignee', models.CharField(max_length=128, verbose_name='下个处理人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('finish_time', models.DateTimeField(auto_now=True, verbose_name='完成时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('suggest', models.CharField(blank=True, max_length=128, null=True, verbose_name='审批结果')),
                ('suggest_content', models.TextField(blank=True, null=True, verbose_name='审批意见')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.wf_business')),
            ],
            options={
                'verbose_name': '工单流程历史_审批中',
                'verbose_name_plural': '工单流程历史_审批中',
            },
        ),
        migrations.CreateModel(
            name='wf_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='上线', max_length=128, verbose_name='请求类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '工单类型',
                'verbose_name_plural': '工单类型',
            },
        ),
        migrations.AddField(
            model_name='wf_info_history_process',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.wf_type', verbose_name='请求类型'),
        ),
        migrations.AddField(
            model_name='wf_info',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.wf_type', verbose_name='请求类型'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='usertype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userType', verbose_name='用户类型'),
        ),
        migrations.AddField(
            model_name='nic',
            name='server_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Server'),
        ),
        migrations.AddField(
            model_name='memory',
            name='server_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Server'),
        ),
        migrations.AddField(
            model_name='handlelog',
            name='creater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userInfo'),
        ),
        migrations.AddField(
            model_name='disk',
            name='server_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Server'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='server_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Server'),
        ),
        migrations.AddField(
            model_name='asset',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='myapp.userInfo', verbose_name='设备管理员'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.wf_business', verbose_name='所属业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Contract', verbose_name='合同'),
        ),
        migrations.AddField(
            model_name='asset',
            name='device_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.DeviceStatus'),
        ),
        migrations.AddField(
            model_name='asset',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.DeviceType'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.IDC', verbose_name='idc机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tag',
            field=models.ManyToManyField(blank=True, to='myapp.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='admininfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserProfile'),
        ),
        migrations.AlterIndexTogether(
            name='server',
            index_together={('sn', 'asset')},
        ),
    ]
