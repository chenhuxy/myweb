#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.utils.safestring import mark_safe


# -------------------------------------pageinfo_search--------------------------------------------------------------------------------------
class pageinfo_search(object):
    def __init__(self, page, count, perItem, keyword):
        self.__page = page
        self.__count = count
        self.__perItem = perItem
        self.__keyword = keyword

    @property
    def start(self):
        start = (self.__page - 1) * self.__perItem
        return start

    @property
    def end(self):
        end = self.__page * self.__perItem
        return end

    @property
    def pageCount(self):
        div = divmod(self.__count, self.__perItem)
        if div[1] == 0:
            pageCount = div[0]
        else:
            pageCount = div[0] + 1
        return pageCount


def pager_user_list_search(request, page, pageCount, keyword):
    page_html = []
    first_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">下页</a>' % (keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/table/user/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_deploy_app_list_search(request, page, pageCount, keyword, ):
    page_html = []
    first_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">下页</a>' % (keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/deploy/app/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_deploy_task_list_search(request, page, pageCount, keyword, ):
    page_html = []
    first_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">下页</a>' % (
            keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/deploy/task/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_wf_list_search(request, page, pageCount, keyword, ):
    page_html = []
    first_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/wf/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">下页</a>' % (keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/wf/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_wf_request_list_search(request, page, pageCount, keyword, ):
    page_html = []
    first_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">下页</a>' % (
            keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/wf/requests/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_assets_asset_search(request, page, pageCount, keyword, ):
    page_html = []
    first_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">首页</a>' % (keyword, 1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">上页</a>' % (keyword, 1,)
    else:
        pre_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">上页</a>' % (keyword, page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">[%d]</a>' % (
                keyword, i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">下页</a>' % (
            keyword, pageCount,)
    else:
        next_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">下页</a>' % (keyword, page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/assets/asset/search_result/keyword=%s&page=%d">尾页</a>' % (keyword, pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


# -------------------------------------pageinfo--------------------------------------------------------------------------------------
class pageinfo(object):
    def __init__(self, page, count, perItem):
        self.__page = page
        self.__count = count
        self.__perItem = perItem

    @property
    def start(self):
        start = (self.__page - 1) * self.__perItem
        return start

    @property
    def end(self):
        end = self.__page * self.__perItem
        return end

    @property
    def pageCount(self):
        div = divmod(self.__count, self.__perItem)
        if div[1] == 0:
            pageCount = div[0]
        else:
            pageCount = div[0] + 1
        return pageCount


def pager_user_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/table/user/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/table/user/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/table/user/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/table/user/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/table/user/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/table/user/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/table/user/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/table/user/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_deploy_task_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/deploy/task/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/deploy/task/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/deploy/task/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/deploy/task/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/deploy/task/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/deploy/task/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/deploy/task/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/deploy/task/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_perm_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/permission/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/permission/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/permission/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/permission/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/permission/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/permission/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/permission/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/permission/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_wf_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/wf/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/wf/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/wf/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/wf/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/wf/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/wf/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/wf/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/wf/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_wf_request_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/wf/requests/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/wf/requests/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/wf/requests/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/wf/requests/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/wf/requests/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/wf/requests/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/wf/requests/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/wf/requests/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_prometheus_alert_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/monitor/prometheus/alert/list/%d">[%d]</a>' % (
                i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/monitor/prometheus/alert/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_skywalking_alert_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/monitor/skywalking/alert/list/%d">[%d]</a>' % (
                i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/monitor/skywalking/alert/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_deploy_app_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/deploy/app/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/deploy/app/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/deploy/app/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/deploy/app/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/deploy/app/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/deploy/app/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/deploy/app/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/deploy/app/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_oplog_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/audit/oplog/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/audit/oplog/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/audit/oplog/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/audit/oplog/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/audit/oplog/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/audit/oplog/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/audit/oplog/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/audit/oplog/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_wf_task_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/wf/tasks/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/wf/tasks/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/wf/tasks/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/wf/tasks/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/wf/tasks/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/wf/tasks/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/wf/tasks/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/wf/tasks/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string


def pager_assets_asset_list(request, page, pageCount):
    page_html = []
    first_html = '<a href="/cmdb/index/assets/asset/list/%d">首页</a>' % (1,)
    page_html.append(first_html)
    if page == 1:
        pre_html = '<a href="/cmdb/index/assets/asset/list/%d">上页</a>' % (1,)
    else:
        pre_html = '<a href="/cmdb/index/assets/asset/list/%d">上页</a>' % (page - 1,)
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
            a_html = '<a style="color:red;"href="/cmdb/index/assets/asset/list/%d">[%d]</a>' % (i + 1, i + 1)
        else:
            a_html = '<a href="/cmdb/index/assets/asset/list/%d">[%d]</a>' % (i + 1, i + 1)
        page_html.append(a_html)
    if page == pageCount:
        next_html = '<a href="/cmdb/index/assets/asset/list/%d">下页</a>' % (pageCount,)
    else:
        next_html = '<a href="/cmdb/index/assets/asset/list/%d">下页</a>' % (page + 1,)
    page_html.append(next_html)
    end_html = '<a href="/cmdb/index/assets/asset/list/%d">尾页</a>' % (pageCount,)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string
