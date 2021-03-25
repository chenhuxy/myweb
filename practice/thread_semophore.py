#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import threading
import time

print('main thread start!')
gl_num = 0
semophore = threading.BoundedSemaphore(5)

def func():
    semophore.acquire()
    global gl_num
    gl_num += 1
    time.sleep(0.001)
    print(gl_num)
    semophore.release()

for i in range(10):
    t = threading.Thread(target=func,)
    t.start()

print('main thread stop!')
