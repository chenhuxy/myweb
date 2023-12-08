#!/usr/bin/env python
# coding:utf-8

import hashlib
import uuid
import random


def get_random_uuid():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode('utf-8')
    md5 = hashlib.md5()  # 2，实例化md5() 方法
    md5.update(uuid_str)  # 3，对字符串的字节类型加密
    result = md5.hexdigest()  # 4，加密
    # print(result)
    return result


def get_random_code(random_length=6):
    code = ''
    # chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    chars = '0123456789'
    length = len(chars) - 1
    for i in range(random_length):
        code += chars[random.randint(0, length)]
    # print(code)
    return code


'''
if __name__ == '__main__':
    get_random_uuid()
'''
