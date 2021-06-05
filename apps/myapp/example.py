#!/usr/bin/env python
#coding:utf-8

from apps.myapp import models
from django.shortcuts import render_to_response
from apps.myapp.login_required import outer


@outer
def layoutsnormal(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-normal.html',msg,)

@outer
def layoutsfixedsidebar(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-fixed-sidebar.html',msg,)

@outer
def layoutsfixedheader(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-fixed-header.html',msg,)

@outer
def layoutshiddensidebar(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/layouts-hidden-sidebar.html',msg,)

@outer
def uialerts(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/alerts.html',msg,)

@outer
def uibuttons(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/buttons.html',msg,)

@outer
def uicards(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/cards.html',msg,)

@outer
def uimodals(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/modals.html',msg,)

@outer
def uitabs(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/tabs.html',msg,)

@outer
def uiprogressbars(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/progress-bars.html',msg,)

@outer
def uiwidgets(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/widgets.html',msg,)

@outer
def chartjs(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/chartjs.html',msg,)

@outer
def forms(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype,'login_user': userDict['user'],}
    return render_to_response('example/forms.html',msg,)

@outer
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

@outer
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

@outer
def pageset(request,*args,**kwargs):
    userinfo = models.userInfo.objects.all()
    usertype = models.userType.objects.all()
    userDict = request.session.get('is_login', None)
    msg = {'userinfo': userinfo, 'usertype': usertype, 'login_user': userDict['user'], }
    return render_to_response('example/settings.html',msg,)