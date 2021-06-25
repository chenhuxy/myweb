#!/usr/bin/env python
#coding:utf-8

from apps.myapp import models
from django.shortcuts import render_to_response
from apps.myapp.auth_helper import custom_login_required


@custom_login_required
def layoutsnormal(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-normal.html',msg,)

@custom_login_required
def layoutsfixedsidebar(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-fixed-sidebar.html',msg,)

@custom_login_required
def layoutsfixedheader(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-fixed-header.html',msg,)

@custom_login_required
def layoutshiddensidebar(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-hidden-sidebar.html',msg,)

@custom_login_required
def uialerts(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/alerts.html',msg,)

@custom_login_required
def uibuttons(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/buttons.html',msg,)

@custom_login_required
def uicards(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/cards.html',msg,)

@custom_login_required
def uimodals(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/modals.html',msg,)

@custom_login_required
def uitabs(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/tabs.html',msg,)

@custom_login_required
def uiprogressbars(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/progress-bars.html',msg,)

@custom_login_required
def uiwidgets(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/widgets.html',msg,)

@custom_login_required
def chartjs(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/chartjs.html',msg,)

@custom_login_required
def forms(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype,'login_user': userDict['user'],}
    return render_to_response('example/forms.html',msg,)

@custom_login_required
def tables(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype,'login_user': userDict['user'],}
    return render_to_response('example/user.html',msg,)



def pageblank(request,*args,**kwargs):
    return render_to_response('example/blank.html')

def pagelogin(request,*args,**kwargs):
    return render_to_response('example/login.html')

def pageregister(request,*args,**kwargs):
    return render_to_response('example/register.html')

@custom_login_required
def pageinvoice(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'],}
    return render_to_response('example/invoice.html',msg,)

def page404(request,*args,**kwargs):
    return render_to_response('example/404.html')

def page500(request,*args,**kwargs):
    return render_to_response('example/500.html')

@custom_login_required
def pageset(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/settings.html',msg,)