#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import redirect,render_to_response,get_object_or_404
from apps.myapp import models
from django.core.exceptions import PermissionDenied

def custom_login_required(main_func):
    def wraper(request,*args,**kwargs):
        if not request.session.get('is_login', None):
            if not request.COOKIES.get('is_login'):
                return redirect('/cmdb/login/')
        return main_func(request,*args,**kwargs)
    return wraper


decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)

@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        username = request.session.get('is_login',None)['user']
        user_obj = get_object_or_404(models.userInfo,username=username)
        #print(user_obj,perm)
        if user_obj.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            #request.user.message_set.create(message = "What are you doing here?!")
            # Return a response or redirect to referrer or some page of your choice
            msg = {'status': '没有权限访问！'}
            return render_to_response('403.html', msg)
    return _function