#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
import time
import json
from django.utils.safestring import mark_safe
from apps.myapp import models
from  apps.myapp import common
from apps.myapp import html_helper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.template import context
from apps.myapp import zabbix
from apps.myapp import prometheus
from apps.myapp import encrypt_helper
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
#from myapp import ansible_api
from django.template import loader,RequestContext
from apps.myapp import token_helper
from apps.myapp import tasks
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
#from apps.myapp import workflow,wf
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow.serializer.prettyxml import XmlSerializer
from SpiffWorkflow import Workflow
#  form upload
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from apps.myapp.login_required import outer

#####################################################################################################################################
from django.shortcuts import render,render_to_response,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import urllib
import urllib.parse


# Create your views here.

# 添加index函数，用于返回index.html页面




def cmdb(request):
    return redirect('/cmdb/index/')

def login(request):
    return render_to_response('backend/login.html')

def logout(request):
    if request.session.get('is_login'):
        del request.session['is_login']
        obj = redirect('/cmdb/login/')
        obj.delete_cookie('is_login')
        #obj.delete_cookie('user')
        #obj.delete_cookie('pass')
    return redirect('/cmdb/login/')

@outer
def index(request):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('backend/index.html',msg,)

#@csrf_protect
def auth(request,*args,**kwargs):
    msg = {'status':''}
    if request.method == 'POST':
        username = request.POST.get('user',None)
        password_origin = request.POST.get('pwd',None)
        password = encrypt_helper.md5_encrypt(password_origin)
        remember = request.POST.get('remember',None)
        is_empty = all([username,password])
        print(username, password_origin,password, remember,is_empty,)
        if is_empty:
            count = models.userInfo.objects.filter(username=username,password=password,status='1').count()
            print(count,)
            if count ==1:
                request.session['is_login'] = {'user': username, 'pass': password, }
                obj = redirect('/cmdb/index/')
                if remember == 'on':
                    obj.set_cookie('is_login','{"user": username, "pass": password, }',3600*24*7,)
                    #obj.set_cookie('user',username,3600*24*7,)
                    #obj.set_cookie('pass',password,3600*24*7,)
                return obj
                #result = {'status':'登录成功！'}
                #return render_to_response('index.html',result)
            else:
                msg = {'status':'用户名密码错误！'}
        else:
            msg = {'status': '用户名或密码不能为空！'}
    else:
        msg = {'status':'无效的请求，请使用post提交！'}
    return render_to_response('backend/login.html',msg,)


def register(request,*args,**kwargs):
    msg = {'status':''}
    if request.method == 'POST':
        username = request.POST.get('user',None)
        password1 = request.POST.get('pwd1',None)
        password2 = request.POST.get('pwd2', None)
        email = request.POST.get('email',None)
        usertype = models.userType.objects.get(name="user")
        group = models.userGroup.objects.get(name="default")
        is_empty = all([username,password1,email])
        if is_empty:
            if password2 == password1:
                is_exist = models.userInfo.objects.filter(username=username)|models.userInfo.objects.filter(email=email)
                if not is_exist:
                    '''
                    # 加载模板
                    template = loader.get_template('email.html')
                    # 渲染模板
                    token = token_helper.get_random_uuid()
                    # email_body = '亲爱的'+username+':<br/>感谢您的注册,请点击下方链接激活账号.<a href="/cmdb/index/table/user/" target="_blank"></a><br/>.'
                    html_str = template.render({"username": username, 'token': token, })
                    print(html_str, type(html_str))
                    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
                    send_mail('【CMDB测试邮件】', '', '834163059@qq.com',
                              [email], fail_silently=False, html_message=html_str)
                    # 记录 token 对应的邮箱是谁 v  k
                    cache.set(token, email, 600)
                    '''
                    tasks.send_email.delay(email, username)
                    password = encrypt_helper.md5_encrypt(password2)
                    models.userInfo.objects.create(username=username,password=password,
                                                   email=email,usertype=usertype,group=group,)
                    msg = {'status':username+',邮件已发送至'+email+',请前往邮箱激活!'}
                    #return render_to_response('register.html', result)
                    #return redirect('/cmdb/login/')
                else:
                    msg = {'status':'该用户已存在！'}
            else:
                msg = {'status':'密码输入不一致！'}
            #return redirect('/login/')
        else:
            msg = {'status':'用户名密码或邮箱不能为空！'}
    #else:
    # result = {'status':'无效的请求，请使用post提交！'}
    return render_to_response('backend/register.html',msg)


def active(request,*args,**kwargs):
    token = kwargs['token']
    # 拿参数对应的缓存数据
    res = cache.get(token)
    #print(res)
    if res:
        # 通过邮箱找到对应用户
        # 给用户的状态字段做更新，从未激活变成激活状态
        username = models.userInfo.objects.filter(email=res).values('username')
        models.userInfo.objects.filter(email=res).update(status='已激活')
        msg = '恭喜你,'+res+'激活成功!'
    else:
        msg = '该链接已经失效！'
    return render_to_response('backend/active.html', {'msg': msg, })


def forget_pass_form_1(request,*args,**kwargs):
    status = ''
    return render_to_response('backend/forget_pass_1.html',{'status':status})

def forget_pass_form_2(request,*args,**kwargs):
    username = request.POST.get('username',None)
    if username:
        is_exist = bool(models.userInfo.objects.filter(username=username))
        print(username,is_exist,type(username),type(is_exist))
        if not is_exist:
            status = '该用户不存在！'
            msg = {'status':status}
            #return render_to_response('forget_pass_2-error.html', msg)
            #return redirect('/cmdb/login/forget_pass/step/1/')
            return render_to_response('backend/forget_pass_1.html', msg)
        else:
            email = models.userInfo.objects.filter(username=username).values('email')
            status = ''
            msg = {'email':email,'username':username,'status':status}
            #return render_to_response('forget_pass_2.html', msg)
            return render_to_response('backend/forget_pass_2.html', msg)
    else:
        status = '用户名不能为空！'
        msg = {'status': status}
        #return render_to_response('forget_pass_2-error.html', msg)
        #return redirect('/cmdb/login/forget_pass/step/1/')
        return render_to_response('backend/forget_pass_1.html', msg)

#@xframe_options_sameorigin
def forget_pass_send(request,*args,**kwargs):
    if request.method=='POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        verify_code = token_helper.get_random_code()
        tasks.send_email_code.delay(email, verify_code)
        request.session['verify_code'] = verify_code
        status = '邮件已发送！'
        #msg = {'status':status,}
        msg = {'status':status,'email':email,'username':username}
        #return redirect('/cmdb/login/forget_pass/send/verify_code=' + verify_code + '&email=' + email)
        return render_to_response('backend/forget_pass_2-send.html',msg)

    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            verify_code = request.session.get('verify_code')
            email = cache.get(verify_code)
            if code == verify_code:
                return redirect('/cmdb/login/forget_pass/change/?verify_code='+verify_code+'&email='+email)
            else:
                status = '验证码错误！'
        else:
            status = '请输入验证码！'
        msg = {'status': status, }
        return render_to_response('backend/forget_pass_2-send.html',msg)


def forget_pass_change(request,*args,**kwargs):
    if request.method=='GET':
        verify_code = request.GET.get('verify_code')
        email = request.GET.get('email')
        request.session['email'] = email
        status = ''
        msg = {'status': status}
    if request.method=='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.session.get('email')
        if password1==password2:
            password = encrypt_helper.md5_encrypt(password2)
            status = '修改成功！'
            msg = {'status':status}
            models.userInfo.objects.filter(email=email).update(password=password,update_time=timezone.now())
    return render_to_response('backend/forget_pass_3.html',msg)


@outer
def userForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
           'login_user': userDict['user'],'status':'', }
    return render_to_response('backend/table_add.html',msg)

@outer
def usertypeForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
           'login_user': userDict['user'],'status':'', }
    return render_to_response('backend/usertype_add.html',msg)

@outer
def usergroupForm_add(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    usergroup = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
           'login_user': userDict['user'],'status':'', }
    return render_to_response('backend/usergroup_add.html',msg)


@outer
def userForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    userid = kwargs['userid']
    obj = models.userInfo.objects.filter(id=userid)
    username = obj.values('username')
    password = obj.values('password')
    email = obj.values('email')
    memo = obj.values('memo')
    usertype_selected = models.userType.objects.filter(userinfo__id=userid)
    usertype = models.userType.objects.all()
    group_selected = models.userGroup.objects.filter(userinfo__id=userid)
    group = models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userid':userid,'username':username,'password':password,'email':email,
           'login_user':userDict['user'],'status':'操作成功','usertype':usertype,
           'usertype_selected':usertype_selected,'group':group,'group_selected':group_selected,
           'memo':memo,}
    print(msg)
    return render_to_response('backend/table_update.html',msg)
    ##return HttpResponse(json.dumps(msg))

@outer
def usertypeForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    usertype = models.userType.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功','usertype':usertype,}
    print(msg)
    return render_to_response('backend/usertype_update.html',msg)

@outer
def usergroupForm_update(request,*args,**kwargs):
    #userid = request.GET.get('userid',None)
    id = kwargs['id']
    usergroup = models.userGroup.objects.filter(id=id)
    userDict = request.session.get('is_login', None)
    msg = {'id':id, 'login_user':userDict['user'],'status':'操作成功','usergroup':usergroup,}
    print(msg)
    return render_to_response('backend/usergroup_update.html',msg)



@outer
def userAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        username = request.POST.get('user',None)
        email = request.POST.get('email',None)
        is_exist = models.userInfo.objects.filter(username=username)|models.userInfo.objects.filter(email=email)
        print(is_exist)
        if not (is_exist):
            password_origin = request.POST.get('pwd', None)
            password = encrypt_helper.md5_encrypt(password_origin)
            print(password,type(password))
            email = request.POST.get('email',None)
            usertype_id = request.POST.get('usertype',None)
            usertype_select = models.userType.objects.get(id=usertype_id)
            group_id = request.POST.get('group', None)
            group_select = models.userGroup.objects.get(id=group_id)
            approval = request.POST.get('approval', None)
            status = request.POST.get('status', None)
            memo = request.POST.get('memo',None)
            is_empty = all([username,password,email,usertype_select,group_select,])
            if is_empty:
                models.userInfo.objects.create(username=username, password=password,
                     email=email,group=group_select,usertype=usertype_select,memo=memo,approval=approval,status=status)
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'添加用户成功', }
                return redirect('/cmdb/index/table/user/')
            else:
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该用户已存在！', }
    return render_to_response('backend/table_add.html',msg)

@outer
def usertypeAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        usertype = request.POST.get('usertype',None)
        is_exist = models.userType.objects.filter(name=usertype)
        print(is_exist)
        if not (is_exist):
            is_empty = all([usertype,])
            if is_empty:
                models.userType.objects.create(name=usertype,)
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'添加用户类型成功', }
                return redirect('/cmdb/index/table/usertype/')
            else:
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该用户类型已存在！', }
    return render_to_response('backend/usertype_add.html',msg)

@outer
def usergroupAdd(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    usergroup = models.userGroup.objects.all()
    #result = {'status': '','usertype':None}
    if request.method == 'POST':
        usergroup = request.POST.get('usergroup',None)
        is_exist = models.userGroup.objects.filter(name=usergroup)
        print(is_exist)
        if not (is_exist):
            leader = request.POST.get('leader',None)
            is_empty = all([usertype,leader])
            if is_empty:
                models.userGroup.objects.create(name=usergroup,leader=leader,)
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'添加用户组成功', }
                return redirect('/cmdb/index/table/usergroup/')
            else:
                msg = {'userinfo': userinfo, 'usertype': usertype,
                       'login_user': userDict['user'],'status':'xx不能为空', }
        else:
            msg = {'userinfo': userinfo, 'usertype': usertype, 'usergroup':usergroup,
                   'login_user': userDict['user'],'status':'该用户组已存在！', }
    return render_to_response('backend/usergroup_add.html',msg)



@outer
def usertype(request,*args,**kwargs):
    usertype=models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'usertype': usertype, 'login_user': userDict['user'],}
    return render_to_response('backend/usertype.html',msg)

@outer
def usergroup(request,*args,**kwargs):
    usergroup=models.userGroup.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'usergroup': usergroup, 'login_user': userDict['user'],}
    return render_to_response('backend/usergroup.html',msg)



def userDel(request,*args,**kwargs):
    id = request.POST.get('userid')
    models.userInfo.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除用户id:'+id,}
    return render_to_response('backend/tables.html',msg)

def usertypeDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.userType.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除用户类型id:'+id,}
    return render_to_response('backend/usertype.html',msg)

def usergroupDel(request,*args,**kwargs):
    id = request.POST.get('id')
    models.userGroup.objects.filter(id=id).delete()
    print('delete',id)
    msg = {'code':1,'result':'删除用户组id:'+id,}
    return render_to_response('backend/usergroup.html',msg)




def userUpdate(request,*args,**kwargs):
    userid = kwargs['userid']
    username = request.POST.get('username')
    password_origin = request.POST.get('password')
    password = encrypt_helper.md5_encrypt(password_origin)
    email = request.POST.get('email')
    usertype = request.POST.get('usertype')
    group = request.POST.get('group')
    memo = request.POST.get('memo')
    update_time = timezone.now()
    print(username,password,email,usertype,group,memo,)
    userDict = request.session.get('is_login', None)
    models.userInfo.objects.filter(id=userid).update(username=username,password=password,
             email=email,usertype=usertype,group=group,memo=memo,update_time=update_time)
    #obj=models.userInfo.objects.filter(id=userid)
    #obj.username = username
    #obj.password = password
    #obj.email = email
    #obj.usertype = usertype
    #obj.save()
    '''
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo':userinfo,'usertype':usertype,'login_user':userDict['user'],'status':'操作成功',}
    print(msg,)
    '''
    return redirect('/cmdb/index/table/user/')
    #return render_to_response('tables.html',msg)
    #return HttpResponse(json.dumps(msg))

def usertypeUpdate(request,*args,**kwargs):
    id = kwargs['id']
    usertype = request.POST.get('usertype')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.userType.objects.filter(id=id).update(name=usertype,update_time=update_time)
    return redirect('/cmdb/index/table/usertype/')

def usergroupUpdate(request,*args,**kwargs):
    id = kwargs['id']
    usergroup = request.POST.get('usergroup')
    leader = request.POST.get('leader')
    update_time = timezone.now()
    userDict = request.session.get('is_login', None)
    models.userGroup.objects.filter(id=id).update(name=usergroup,leader=leader,update_time=update_time)
    return redirect('/cmdb/index/table/usergroup/')




def search(request,*args,**kwargs):
    keyword = request.POST.get('keyword').strip()
    page = '1'
    print(keyword,page)
    if (keyword):
        return redirect('/cmdb/index/table/user/search_result/keyword=' + keyword + '&page=' + page)
    else:
        return redirect('/cmdb/index/table/user/')

@outer
def search_result(request,*args,**kwargs):
    keyword = kwargs['keyword']
    userinfo = models.userInfo.objects.filter(username__icontains=keyword) | models.userInfo.objects.filter(
        email__icontains=keyword)
    count = userinfo.count()
    userDict = request.session.get('is_login', None)
    page = common.try_int(kwargs['page'], 1)
    print(keyword,page)
    perItem = common.try_int(request.COOKIES.get('page_num', 10), 10)
    pageinfo = html_helper.pageinfo_search(page, count, perItem,keyword)
    userinfo = userinfo[pageinfo.start:pageinfo.end]
    page_string = html_helper.pager_search(request, page, pageinfo.pageCount,keyword)
    msg = {'userinfo': userinfo, 'login_user': userDict['user'], 'status': '操作成功',
           'count': count, 'pageCount': pageinfo.pageCount, 'page': page_string, }
    #return render_to_response('table_search.html',msg)
    return render_to_response('backend/tables.html', msg)


@outer
def tables(request,*args,**kwargs):
    #try:
    #    page = int(page)
    #except:
    #    page = 1
    #perItem = 10
    page = common.try_int(kwargs['page'],1)
    perItem = common.try_int(request.COOKIES.get('page_num',10),10)
    count = models.userInfo.objects.all().count()
    pageinfo = html_helper.pageinfo(page,count,perItem)
    userinfo = models.userInfo.objects.all()[pageinfo.start:pageinfo.end]
    page_string= html_helper.pager(request,page,pageinfo.pageCount)
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login',None)
    #if not userDict:
    #    return redirect('/cmdb/login/')
    msg = {'userinfo': userinfo, 'usertype': usertype, 'count': count, 'pageCount': pageinfo.pageCount,
           'page': page_string,'login_user': userDict['user'], }
    response= render_to_response('backend/tables.html',msg,)
    #response.set_cookie('k1','v1')
    #print(request.COOKIES)
    #print(request.COOKIES.get('page_num'))
    #print(args,kwargs)
    return response



##################################################################################################################################
'''
@api_view(['GET', 'PUT', 'DELETE','POST'])
def index(request):
    print (request.method)
    print (request.data)
    return Response([{'asset':'1','request_hostname':'c1.puppet.com'}])
'''


@api_view(['GET','POST','PUT','DELETE'])
def serverinfo(request):
    print(request.POST)
    print(request.method)
    if request.method == 'POST':
        print(urllib.parse.unquote(request.data))
        print(request.data)
    return Response('receive ok!')

def ansible_test(request,*args,**kwargs):
    resource = [
        {'hostname': 'localtest', 'ip': '192.168.209.128', 'username': 'root', 'password': 'redhat'},
        {'hostname': 'localtest2', 'ip': '192.168.178.141', 'username': 'root', 'password': 'yyy'}
        # 有个小坑，hostname中不能有空格，否则这个host会被ansible无视
    ]
    api = ansible_api.AnsibleAPI(resource)
    # 开始模拟以ad-hoc方式运行ansible命令
    api.run(
        ['localtest', 'localtest2'],  # 指出本次运行涉及的主机，在resource中定义
        'command',  # 本次运行使用的模块
        'hostname'  # 模块的参数
    )

    # 获取结果，是一个字典格式，如果是print可以用json模块美化一下
    import json
    print(json.dumps(api.get_result(), indent=4))



