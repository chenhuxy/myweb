#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.utils.safestring import mark_safe

class pageinfo(object):
    def __init__(self,page,count,perItem):
        self.__page = page
        self.__count = count
        self.__perItem = perItem

    @property
    def start(self):
        start = (self.__page-1)*self.__perItem
        return  start

    @property
    def end(self):
        end = self.__page*self.__perItem
        return  end

    @property
    def pageCount(self):
        div = divmod(self.__count,self.__perItem)
        if div[1] == 0:
            pageCount = div[0]
        else:
            pageCount = div[0] + 1
        return pageCount


def pager(request,page,pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/table/user/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/table/user/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/table/user/%d">上页</a>' % (page - 1,)
    page_html.append(pre_html)

    pageDisplay = 11
    pageStart = int((page - (pageDisplay + 1) / 2))
    pageEnd = int(page + (pageDisplay - 1) / 2)
    if pageCount < pageDisplay:
        pageStart = 0
        pageEnd = pageCount
    else:
        if page < (pageDisplay + 1) / 2:
            pageStart = 0
            pageEnd = pageDisplay
        else:
            if pageEnd > pageCount:
                pageStart = pageStart
                pageEnd = pageCount
    for i in range(pageStart, pageEnd):
        if page == i + 1:
            a_html = '<a style="color:red;"href="/cmdb/index/table/user/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/table/user/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/table/user/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/table/user/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/table/user/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


class pageinfo_search(object):
    def __init__(self,page,count,perItem,keyword):
        self.__page = page
        self.__count = count
        self.__perItem = perItem
        self.__keyword = keyword

    @property
    def start(self):
        start = (self.__page-1)*self.__perItem
        return  start

    @property
    def end(self):
        end = self.__page*self.__perItem
        return  end

    @property
    def pageCount(self):
        div = divmod(self.__count,self.__perItem)
        if div[1] == 0:
            pageCount = div[0]
        else:
            pageCount = div[0] + 1
        return pageCount



def pager_search(request,page,pageCount,keyword,):

    page_html = []
    first_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">首页</a>' % (keyword,1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">上页</a>' % (keyword,1,)
    else:
        pre_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">上页</a>' % (keyword,page - 1,)
    page_html.append(pre_html)

    pageDisplay = 11
    pageStart = int((page - (pageDisplay + 1) / 2))
    pageEnd = int(page + (pageDisplay - 1) / 2)
    if pageCount < pageDisplay:
        pageStart = 0
        pageEnd = pageCount
    else:
        if page < (pageDisplay + 1) / 2:
            pageStart = 0
            pageEnd = pageDisplay
        else:
            if pageEnd > pageCount:
                pageStart = pageStart
                pageEnd = pageCount
    for i in range(pageStart, pageEnd):
        if page == i + 1:
            a_html = '<a style="color:red;"href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">[%d]</a>' % (keyword,i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">[%d]</a>' % (keyword,i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">下页</a>' % (keyword,pageCount,)
    else:
        next_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">下页</a>' % (keyword,page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">尾页</a>' % (keyword,pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string