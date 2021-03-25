#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
import threading
import time

def show(arg):
    time.sleep(0.001)
    print('thread'+str(arg))

print('main thread start!')

for i in range(10):
    t= threading.Thread(target=show,args=(i,))
    #t.setDaemon(daemonic=True)
    t.start()
    #t.join()   #顺序执行

print('main thread stop!')
'''
import threading
import time

def show(arg):
    time.sleep(0.1)
    print('thread'+str(arg))

print('main thread start!')
threads = []
for i in range(10):
    t = threading.Thread(target=show,args=(i,))
    threads.append(t)
    t.start()
for i in threads:
    t.join()       #顺序退出
print('main thread stop!')