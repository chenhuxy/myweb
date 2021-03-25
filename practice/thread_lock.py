#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
import threading
import time

print('main thread start!')
gl_num = 0
def show(arg):
    global gl_num
    #time.sleep(1)
    gl_num += 1
    time.sleep(0.0001)
    print(gl_num)

for i in range(10):
    t= threading.Thread(target=show,args=(i,))
    t.start()

print('main thread stop!')
'''

import threading
import time

print('main thread start!')
gl_num = 0
lock = threading.RLock()

def func():
    lock.acquire()
    global gl_num
    gl_num += 1
    time.sleep(1)
    print(gl_num)
    lock.release()

for i in range(10):
    t = threading.Thread(target=func,)
    t.start()

print('main thread stop!')