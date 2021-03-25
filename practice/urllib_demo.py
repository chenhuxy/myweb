#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import urllib.request
import re
import os
import time


def urlOpen(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/\
                    537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
    data = urllib.request.urlopen(req).read()
    return data

def findImage(url):
    html = urlOpen(url).decode('utf-8')
    image = r'<img src="([^"]+\.jpg)"'
    addr = re.findall(image,html)
    return addr

def downloadImage(dir='picture'):
    os.mkdir(dir)
    os.chdir(dir)
    page = 1
    x = 0
    imageUrl = []
    while page <= 1:
        urls = url + 'a/more_' + str(page) + '.html'
        addrs = findImage(urls)
        imageUrl.append(addrs)
        print(len(addrs))
        for i in imageUrl:
            print(i)
        page += 1
        time.sleep(20)
    for i in imageUrl:
        filename = str(x) + '.' + i.split('.')[-1]
        x += 1
        with open(filename,'wb') as f:
            f = urlOpen(i)
            f.write(i)

if __name__ == '__main__':
    url = 'http://www.meizitu.com/'
    downloadImage()




