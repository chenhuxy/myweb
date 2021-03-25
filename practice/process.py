#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
import threading
from multiprocessing import Process
import time


def foo(i):
    #time.sleep(10)
    print('say hello,'+str(i))
if __name__ == '__main__':
    print('main process start!')
    for i in range(10):
        p = Process(target=foo,args=(i,))
        p.start()
        #p.join()
    print('main process stop!')



from multiprocessing import Process
from multiprocessing import Queue
#from queue import Queue
import time

def foo(i,q):
    q.put('process'+str(i))
    #time.sleep(1)
    print(i,q.get())
if __name__ == '__main__':
    print('main process start!')
    Q = Queue()
    Q.put('mainProcess')
    for i in range(10):
        p = Process(target=foo,args=(i,Q,))
        p.start()
        p.join()
    print('main process queue:',Q.get())
    print('main process stop!')
'''

from multiprocessing import Process
from multiprocessing import Pool
import time

def foo(i):
    time.sleep(1)
    return i+100

def bar(arg):
    print(arg)

if __name__ == '__main__':
    pool = Pool(5)

    for i in range(10):
        pool.apply_async(func=foo,args=(i,),callback=bar)
    print(pool.apply_async(func=foo, args=(i,)).get())
    print('end')
    pool.close()
    pool.join()



