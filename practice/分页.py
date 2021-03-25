#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.utils.safestring import mark_safe

class PageInfo(object):
    def __init__(self,current,totalItem,perItem=5):
        self.__current = current
        self.__totalItem = totalItem
        self.__perItem = perItem
    def From(self):
        return (self.__current-1)*self.__perItem+1
    def To(self):
        return self.__current*self.__perItem
    def TotalPage(self):
        result = divmod(self.__totalItem,self.__perItem)
        if result[1] ==0:
            return result[0]
        else:
            return result[0]+1

def CustomPager(baseurl,currentPage,totalPage):
    perPage = 11
    begin = 1
    end = 1
    if totalPage <= perPage:
        begin = begin
        end = totalPage
    else:
        if currentPage >= (perPage+1)/2:
            begin = currentPage-5
            end = currentPage+5
            if end >= totalPage:
                end = totalPage
        else:
            begin = begin
            end = perPage
    page_list = []
    if currentPage <= begin:
        first = "<a href=''>首页</a>"
    else:
        first = "<a href='%s%d'>首页</a>" %(baseurl,begin)
    page_list.append(first)
    if currentPage <= begin:
        prev = "<a href=''>上一页</a>"
    else:
        prev = "<a href='%s%d'>上一页</a>" %(baseurl,currentPage-1)
    page_list.append(prev)
    for page in range(begin,end):
        if page == currentPage:
            temp = "<a href='%s%d' class='selected'>%d</a>" %(baseurl,page,page)
        else:
            temp = "<a href='%s%d'>%d</a>" %(baseurl,page,page)
    if currentPage >=totalPage:
        post = "<a href='#'>下一页</a>"
    else:
        post = "<a href='%s%d'>下一页</a>" %(baseurl,currentPage+1)
    page_list.append(post)
    if currentPage >= totalPage:
        last = "<a href=''>尾页</a>"
    else:
        last = "<a href='%s%d'>尾页</a>" % (baseurl, totalPage)
    page_list.append(last)
    result = ''.join(page_list)
    data =  mark_safe(result)
    return data
    print(data)



