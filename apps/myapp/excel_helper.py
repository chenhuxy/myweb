#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import logging
import os
from xlutils.copy import copy

import xlrd
import xlwt
import pytz
from datetime import datetime


def read_excel(file_name, sheet_name):
    workbook = xlrd.open_workbook(file_name)
    # 读取第一个sheet
    # sheet = workbook.sheet_by_index(0)
    # 通过sheet名称查找
    sheet = workbook.sheet_by_name(sheet_name)
    rows = sheet.nrows
    cols = sheet.ncols
    data = []
    print("\033[42m 开始读取配置：%s \033[0m" % file_name)
    logging.info("\033[42m 开始读取配置：%s \033[0m" % file_name)
    print("\033[42m 总行数：%d，总列数：%d \033[0m" % (rows, cols))
    logging.info("\033[42m 总行数：%d，总列数：%d \033[0m" % (rows, cols))
    for i in range(2, rows):
        print("\033[42m==========>行号：%d\033[0m" % (i + 1))
        logging.info("\033[42m==========>行号：%d\033[0m" % (i + 1))
        row_val = []
        for j in range(cols):
            # 判断python读取的excel单元格返回类型，0：empty，1：string，2：number（float），3：date，4：boolean，5：error
            cell_type = sheet.cell(i, j).ctype
            # 获取单元格的值
            cell_val = sheet.cell(i, j).value
            # 数字类型转换为字符串类型
            if cell_type == 2:
                cell_val = str(int(cell_val))
            else:
                cell_val = cell_val
            row_val.append(cell_val)
        data.append(row_val)
        # print row_val,type(row_val)
        # 打印中文字符
        # print("\033[42m 行数据：%s \033[0m" % (json.dumps(row_val).decode('unicode-escape')))
        # logging.info("\033[42m 行数据：%s \033[0m" % (json.dumps(row_val).decode('unicode-escape')))
        print("\033[42m 行数据：%s \033[0m" % (json.dumps(row_val)))
        logging.info("\033[42m 行数据：%s \033[0m" % (json.dumps(row_val)))
        '''	
        row_val = sheet.row_values(i)
        data.append(row_val)
        print ("\033[42m 行数据：%s \033[0m" %(row_val))
        logging.info( "\033[42m 行数据：%s \033[0m" %(row_val))
        '''
    # print sheet.row_values(1)[1],type(sheet.row_values)
    return data


def convert_to_eastern_time(dt):
    # Convert datetime to UTC
    utc_dt = dt.astimezone(pytz.utc)
    # Convert UTC to Eastern Time (UTC-5)
    eastern_tz = pytz.timezone('Asia/Shanghai')  # Assuming Shanghai time is equivalent to China Standard Time (CST)
    eastern_dt = utc_dt.astimezone(eastern_tz)
    return eastern_dt

# .xlsx Not Supported


def write_excel(dest_file, sheet_name, row_num, data_list):
    # Check if the file exists
    if os.path.exists(dest_file):
        # If the file exists, open it and get the workbook object
        workbook = xlrd.open_workbook(dest_file, formatting_info=True)
        workbook_copy = copy(workbook)
        sheet = workbook_copy.get_sheet(0)
    else:
        # If the file doesn't exist, create a new workbook
        workbook_copy = xlwt.Workbook()
        sheet = workbook_copy.add_sheet(sheet_name)

    # Define datetime style
    style = xlwt.XFStyle()
    style.num_format_str = 'yyyy-mm-dd hh:mm:ss.000'

    # Iterate through the data list and write to the appropriate cells
    for i, data in enumerate(data_list):
        if isinstance(data, datetime):
            # Convert datetime to Eastern Time
            data = convert_to_eastern_time(data)
            # Convert datetime to string with the desired format
            data_str = data.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Drop microseconds
            # Write datetime data as string with custom style
            sheet.write(row_num, i, data_str, style)
        else:
            # Write other data types normally
            sheet.write(row_num, i, data)

    # Save the workbook to the destination file
    workbook_copy.save(dest_file)
