#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import redirect

def outer(main_func):
    def wraper(request,*args,**kwargs):
        if not request.session.get('is_login', None):
            if not request.COOKIES.get('is_login'):
                return redirect('/cmdb/login/')
        return main_func(request,*args,**kwargs)
    return wraper
    print(args,kwargs)