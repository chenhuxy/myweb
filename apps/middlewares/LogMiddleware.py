#!/usr/bin/env python
# coding:utf-8


import json
import time

from django.utils.deprecation import MiddlewareMixin
from apps.myapp.models import OpLogs
from apps.myapp import encrypt_helper


class OpLog(MiddlewareMixin):
    __exclude_urls = ['/cmdb/index/deploy/task/get_task_info/', '/admin/', '/static/']  # 定义不需要记录日志的url

    def __init__(self, *args):
        super(OpLog, self).__init__(*args)

        self.start_time = None  # 开始时间
        self.end_time = None  # 响应时间
        self.data = {}  # dict数据

    def process_request(self, request):
        """
        请求进入
        :param request: 请求对象
        :return:
        """

        self.start_time = time.time()  # 开始时间
        re_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 请求时间（北京）

        # 请求IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # 如果有代理，获取真实IP
            re_ip = x_forwarded_for.split(",")[0]
        else:
            re_ip = request.META.get('REMOTE_ADDR')

        # 请求方法
        re_method = request.method

        # 请求参数
        re_content = request.GET if re_method == 'GET' else request.POST
        # 筛选空参数
        if re_content:
            # 加密请求参数敏感信息
            if 'pwd' in re_content:
                # print(re_content, re_content['pwd'], type(re_content['pwd']))
                # This QueryDict instance is immutable
                re_content = re_content.copy()
                # re_content['pwd'] = encrypt_helper.md5_encrypt(re_content['pwd'])
                re_content['pwd'] = "***"
            re_content = json.dumps(re_content)
        else:
            re_content = None

        re_user = request.session.get('is_login', None)
        if re_user:
            re_user = re_user['user']
        else:
            re_user = 'AnonymousUser'

        self.data.update(
            {
                're_time': re_time,  # 请求时间
                're_url': request.path,  # 请求url
                're_method': re_method,  # 请求方法
                're_ip': re_ip,  # 请求IP
                're_content': re_content,  # 请求参数
                're_user': re_user  # 操作人(需修改)，网站登录用户
                # 're_user': 'AnonymousUser'  # 匿名操作用户测试
            }
        )

    def process_response(self, request, response):
        """
        响应返回
        :param request: 请求对象
        :param response: 响应对象
        :return: response
        """
        # 请求url在 exclude_urls中，直接return，不保存操作日志记录
        for url in self.__exclude_urls:
            if url in self.data.get('re_url'):
                return response

        # 获取响应数据字符串(多用于API, 返回JSON字符串)
        rp_content = response.content.decode()
        self.data['rp_content'] = rp_content

        # 状态码
        self.data['rp_status_code'] = response.status_code

        # 耗时
        self.end_time = time.time()  # 响应时间
        rp_duration = self.end_time - self.start_time
        self.data['rp_duration'] = round(rp_duration * 1000)  # 耗时毫秒/ms

        OpLogs.objects.create(**self.data)  # 操作日志入库db

        return response
