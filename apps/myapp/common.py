#!/usr/bin/env python
# _*_ coding:utf-8 _*_

def try_int(arg,default):
    try:
        arg = int(arg)
    except:
        arg = default
    return arg