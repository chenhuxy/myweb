#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from greenlet import greenlet

def test1():
    print('test1-11')
    gr2.switch()
    print('test1-22')
    gr2.switch()

def test2():
    print('test2-33')
    gr1.switch()
    print('test2-44')

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
