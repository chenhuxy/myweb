#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from datetime import datetime, timedelta
import pytz


def try_int(arg, default):
    try:
        arg = int(arg)
    except:
        arg = default
    return arg


def time_tz_fmt(utc_timestamp_str):
    # 输入UTC时间戳字符串
    # utc_timestamp_str = "2024-01-22T08:58:37.163435432Z"
    utc_timestamp_str = utc_timestamp_str
    # The fromisoformat method was introduced in Python 3.7
    # utc_timestamp = datetime.fromisoformat(utc_timestamp_str.replace("Z", "+00:00"))
    # 使用 strptime 解析时间字符串
    utc_timestamp_str = utc_timestamp_str[:19]  # Remove 'Z' at the end
    utc_timestamp = datetime.strptime(utc_timestamp_str, "%Y-%m-%dT%H:%M:%S")

    # 设置UTC时区
    utc_timezone = pytz.timezone("UTC")
    utc_time = utc_timezone.localize(utc_timestamp)

    # 转换为东八区时区
    eastern_timezone = pytz.timezone("Asia/Shanghai")
    eastern_time = utc_time.astimezone(eastern_timezone)

    # 返回天真的（naive）datetime对象
    naive_eastern_time = eastern_time.replace(tzinfo=None)

    print("UTC时间:", utc_time)
    print("东八区时间:", eastern_time)
    print("天真东八区时间:", naive_eastern_time)
    # return eastern_time
    return naive_eastern_time
