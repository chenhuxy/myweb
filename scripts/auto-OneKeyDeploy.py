#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
author: chenhu
date: 2023/06/15
'''

import urllib 
import urllib2 
#import requests
import random 
import uuid
import time
import sys
from threading import Thread
import json
import zipfile
import os
import subprocess
import shutil
from glob import glob
import datetime
import xlrd 
#1.2.0,使用最新版本报错 
#sudo pip install xlrd==1.2.0 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
import logging
import contextlib
#使用Python 2.6运行Python 2.7代码
#AttributeError: ZipFile instance has no attribute '__exit__'


#Excel sheet名使用中文
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


'''
#定义发布配置，已使用读取excel代替

project_list = [{"name": "core-start", "id": "119", "tag": "tag_20230608"},
		{"name": "mobile-start", "id": "91", "tag": "tag_20230608"},
		{"name": "data-batch", "id": "30", "tag": "tag_20230526"},
		{"name": "clearing-start", "id": "118", "tag": "tag_20230615"},
		{"name": "dubbo", "id": "121", "tag": "release"},
]
'''

##定义全局变量

#jdk7编译的老项目
project_tomcat = ["passengerCar","passengerCar_zczr","heavyTruck","heavyTruck_zczr",] 
#滚动发布的项目
project_tomcat_rollupdate = ["passengerCar","heavyTruck",] 
#gitlab主机地址
host = "http://gitlab.utfinancing.com"
#下载目录
download_base_dir = "/tmp/"
#解压目录
unzip_base_dir = "/tmp/"
#发布目录
deploy_dir = "/etc/ansible/roles/"
#配置目录
conf_dir = "./conf"
#日志目录
log_base_dir = "./logs"
#自定义header
my_headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	"PRIVATE-TOKEN": "glpat-kqPgKptRo6_ekUAiBvHb",
}


def get_project_name(project_id):
	url = host +  "/api/v4/projects/" + str(project_id)
	request =  urllib2.Request(url=url, headers=my_headers)
	response = urllib2.urlopen(request)
	#print response.read().split('path')[1].split('"')[2],type(response.read())
	project_name = response.read().split('path')[1].split('"')[2]
	return project_name

def chunk_report(bytes_so_far, chunk_size, total_size):
	percent = float(bytes_so_far) / total_size
	percent = round(percent*100, 2)
	if percent %1==0:
		sys.stdout.write("----------------------已下载 %d 字节，总共 %d 字节 (下载进度为：%0.2f%%)-------------------" % (bytes_so_far, total_size, percent))
		logging.info("----------------------已下载 %d 字节，总共 %d 字节 (下载进度为：%0.2f%%)-------------------" % (bytes_so_far, total_size, percent))
	if bytes_so_far >= total_size:
		sys.stdout.write('下载完成')
		logging.info('下载完成')		

def chunk_read(response, url,chunk_size=65536, report_hook=None):
	total_size = response.info().getheader('Content-Length').strip()
	total_size = int(total_size)
	bytes_so_far = 0
	path_name = url.split("/")[-5]
	path_name = path_name.replace("\n","")
	path_name = path_name.decode("utf-8")
	project_name = get_project_name(path_name)
	project_name_zip = get_project_name(path_name) + ".zip"
	print "\033[42m %s 开始下载，下载目录：%s---------------------------------------------------->\033[0m" %(project_name_zip,download_dir)
	logging.info("\033[42m %s 开始下载，下载目录：%s---------------------------------------------------->\033[0m" %(project_name_zip,download_dir))
	if not os.path.exists(download_dir):
		os.makedirs(download_dir)
	with open("%s" %(os.path.join(download_dir,project_name_zip)), "wb") as f:
		while True:
			chunk = response.read(chunk_size)
			f.write(chunk)
			f.flush() 
			bytes_so_far += len(chunk)
			if not chunk:
				break
			if report_hook:
				report_hook(bytes_so_far, chunk_size, total_size)
	return bytes_so_far


def unzip_project_artifact(file_name):
	if not os.path.exists(unzip_dir):
		os.makedirs(unzip_dir)
	#with zipfile.ZipFile(os.path.join(download_dir,file_name), 'r') as zip_ref:
	with contextlib.closing(zipfile.ZipFile(os.path.join(download_dir,file_name), 'r')) as zip_ref:
		zip_ref.extractall(unzip_dir)  # 解压路径为/tmp目录
		print "\033[42m 解压 %s 至目录：%s \033[0m" %(file_name,unzip_dir)
		logging.info( "\033[42m 解压 %s 至目录：%s \033[0m" %(file_name,unzip_dir))

def publish(src_file,deploy_dir):
	if not os.path.isfile(src_file):
		print "\033[41m" + src_file + " 不存在!!!\033[0m"
		logging.error( "\033[41m" + src_file + " 不存在!!!\033[0m")
	else:
		fpath,fname = os.path.split(src_file)
		if not os.path.exists(deploy_dir):
			os.makedirs(deploy_dir)
		shutil.move(src_file,deploy_dir + fname)
		print "\033[42m 移动 %s -> %s \033[0m" %(src_file,deploy_dir + fname)
		logging.info( "\033[42m 移动 %s -> %s \033[0m" %(src_file,deploy_dir + fname))

def download_project_artifact(url,pkg_name):
	#print url
	request =  urllib2.Request(url=url, headers=my_headers)
	try:
		response = urllib2.urlopen(request);
		chunk_read(response,url, report_hook=chunk_report)
		path_name = url.split("/")[-5]
		path_name = path_name.replace("\n","")
		path_name = path_name.decode("utf-8")
		project_name = get_project_name(path_name)
		project_name_zip = get_project_name(path_name) + ".zip"
		print "\033[42m %s 下载完成，下载目录：%s\033[0m" %(project_name_zip,download_dir)
		logging.info( "\033[42m %s 下载完成，下载目录：%s\033[0m" %(project_name_zip,download_dir))
		unzip_project_artifact(project_name_zip)
		bak(deploy_dir + pkg_name + "/files/" + get_sub_dirs(unzip_dir,[])[0].split('/')[-1],pkg_name)
		publish(get_sub_dirs(unzip_dir,[])[0],deploy_dir + pkg_name + "/files/" )
	except:
		response = None
	return response

def clean(dirs):
	if not os.path.exists(dirs):
		return False
	if os.path.isfile(dirs):
		os.remove(dirs)
		return
	for i in os.listdir(dirs):
		t = os.path.join(dirs,i)
		if os.path.isdir(t):
			clean(t)
		else:
			os.unlink(t)
	if os.path.exists(dirs):
		os.removedirs(dirs)
	print "\033[42m 删除成功!!! %s\033[0m" %(dirs)
	logging.info( "\033[42m 删除成功!!! %s\033[0m" %(dirs))

def bak(src_file,pkg_name):
	if not os.path.isfile(src_file):
		print "\033[43m" + src_file + " 不存在！跳过备份步骤。\033[0m"
		logging.warning( "\033[43m" + src_file + " 不存在！跳过备份步骤。\033[0m")
	elif not os.path.isfile(src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d")):
		os.rename(src_file,src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d"))
		print "\033[42m 重命名 %s -> %s \033[0m" %(src_file,src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d"))
		logging.info( "\033[42m 重命名 %s -> %s \033[0m" %(src_file,src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d")))
	else:
		print "\033[43m 备份文件 %s 已存在，无需再备份！！！ \033[0m" %(src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d"))
		logging.warning( "\033[43m 备份文件 %s 已存在，无需再备份！！！ \033[0m" %(src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d")))
	#清除旧的备份
	for i in glob(deploy_dir + pkg_name + "/files/*"):
		if i not in (src_file,src_file + "-bak-" + datetime.date.today().strftime("%Y-%m-%d")):
			os.remove(i)
			print "\033[42m 删除备份文件 %s \033[0m" %(i)
			logging.info("\033[42m 删除备份文件 %s \033[0m" %(i))
			
	
def get_sub_dirs(dirs,list_name):
	if not os.path.exists(dirs):
		return False
	if os.path.isfile(dirs):
		return False
	for i in os.listdir(dirs):
		t = os.path.join(dirs,i)
		if os.path.isdir(t):
			get_sub_dirs(t,list_name)
		else:
			list_name.append(t)
	return list_name

def deploy(service_name):
	print "\033[42m 开始发布服务：%s \033[0m" %(service_name)
	logging.info( "\033[42m 开始发布服务：%s \033[0m" %(service_name))
	if service_name in project_tomcat_rollupdate:
		#ret = os.system("python /etc/ansible/tools/deploy.py " + service_name)
		#subprocess.check_call执行错误则中断后面的执行抛出异常
		#ret = subprocess.check_call(["/etc/ansible/tools/deploy.py",service_name])
		#ret = subprocess.call(["/etc/ansible/tools/deploy.py",service_name])
		# 主进程获取子进程stdout，stderr
		ret = subprocess.Popen(["/etc/ansible/tools/deploy.py",service_name],shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	else:
		#ret = os.system("ansible-playbook /etc/ansible/" + service_name + ".yml")
		#subprocess.check_call执行错误则中断后面的执行抛出异常
		#ret = subprocess.check_call(["ansible-playbook","/etc/ansible/" + service_name + ".yml"])
		#ret = subprocess.call(["ansible-playbook","/etc/ansible/" + service_name + ".yml"])
		# 主进程获取子进程stdout，stderr
		ret = subprocess.Popen(["ansible-playbook","/etc/ansible/" + service_name + ".yml"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while ret.poll() is None:
		line = ret.stdout.readline()
		line = line.strip()
		if line:
			print line
			logging.info(line)
	if ret.returncode == 0:
		#print "\033[42m 发布脚本执行成功，返回值：%s \033[0m" %(ret.returncode)
		#logging.info( "\033[42m 发布脚本执行成功，返回值：%s \033[0m" %(ret.returncode))
		print "发布脚本执行成功，返回值：%s" %(ret.returncode)
		logging.info( "发布脚本执行成功，返回值：%s" %(ret.returncode))
	else:
		#print "\033[41m 发布脚本执行失败，返回值：%s \033[0m" %(ret.returncode)
		print "发布脚本执行失败，返回值：%s" %(ret.returncode)
		#logging.error( "\033[41m 发布脚本执行失败，返回值：%s \033[0m" %(ret.returncode))
		logging.error( "发布脚本执行失败，返回值：%s" %(ret.returncode))
	'''
	if ret == 0:
		print "\033[42m 发布脚本执行成功，返回值：%s \033[0m" %(ret)
		logging.info( "\033[42m 发布脚本执行成功，返回值：%s \033[0m" %(ret))
	else:
		print "\033[41m 发布脚本执行失败，返回值：%s \033[0m" %(ret)
		logging.error( "\033[41m 发布脚本执行失败，返回值：%s \033[0m" %(ret))
	'''


def read_excel(file_name):
	workbook = xlrd.open_workbook(file_name)
	#读取第一个sheet
	#sheet = workbook.sheet_by_index(0)
	#通过sheet名称查找
	sheet = workbook.sheet_by_name('服务发布列表')
	rows = sheet.nrows
	cols = sheet.ncols
	data = []
	print "\033[42m 开始读取配置：%s \033[0m" %(file_name)
	logging.info( "\033[42m 开始读取配置：%s \033[0m" %(file_name))
	print "\033[42m 总行数：%d，总列数：%d \033[0m" %(rows,cols)
	logging.info( "\033[42m 总行数：%d，总列数：%d \033[0m" %(rows,cols))
	for i in range(2,rows):
		print "\033[42m==========>行号：%d\033[0m" %(i+1)
		logging.info( "\033[42m==========>行号：%d\033[0m" %(i+1))
		row_val = []
		for j in range(cols):
			#判断python读取的excel单元格返回类型，0：empty，1：string，2：number（float），3：date，4：boolean，5：error
			cell_type = sheet.cell(i,j).ctype
			#获取单元格的值
			cell_val = sheet.cell(i,j).value
			#数字类型转换为字符串类型
			if cell_type == 2:
				cell_val = str(int(cell_val))
			else:
				cell_val = cell_val
			row_val.append(cell_val)
		data.append(row_val)
		#print row_val,type(row_val)
		#打印中文字符
		print "\033[42m 行数据：%s \033[0m" %(json.dumps(row_val).decode('unicode-escape'))
		logging.info( "\033[42m 行数据：%s \033[0m" %(json.dumps(row_val).decode('unicode-escape')))
		'''	
		row_val = sheet.row_values(i)
		data.append(row_val)
		print "\033[42m 行数据：%s \033[0m" %(row_val)
		logging.info( "\033[42m 行数据：%s \033[0m" %(row_val))
		'''
	#print sheet.row_values(1)[1],type(sheet.row_values)
	return data

def log_to_file(logs_dir):
	if not os.path.exists(logs_dir):
		os.makedirs(logs_dir)
	logging.basicConfig(
		#filename = logs_dir + "/" + os.path.basename(__file__).split('.')[0] + ".log",
		filename = logs_dir.rstrip("/") + "/" + os.path.basename(__file__).split('.')[0] + "-" + sys.argv[4] + ".log",
		level = logging.DEBUG,
		format = '%(asctime)s %(thread)d %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
		#a：代表每次运行程序都继续写log，即不覆盖之前保存的log信息；w：代表每次运行程序都重新写log，即覆盖之前保存的log信息。
		filemode = 'w'
	)

def get_job_name(project_name):
	if project_name in project_tomcat:
		job = "build_java_prod"
	else:
		job = "build_java"
	return job 

def format_conf_dir(conf_dir):
	conf_dir = conf_dir.rstrip("/")
	if not os.path.exists(conf_dir):
		os.makedirs(conf_dir)
	return conf_dir
	

if __name__ == '__main__':
	'''
	for item in project_list:	
		#print item,type(item)
		gitlab_url = host + "/api/v4/projects/" + str(item['id']) + "/jobs/artifacts/" + item['tag'] + "/download?job=" + job
		download_project_artifact(gitlab_url,item['name'])
		clean(download_dir)	
		clean(unzip_dir)	
		deploy(item['name'])
	'''
	try:
		log_to_file(log_base_dir.rstrip("/") + "/" + sys.argv[2])
		#conf_dir = format_conf_dir(conf_dir)
		'''
		project_list = read_excel(conf_dir + "/发布配置.xlsx")
		#print project_list,type(project_list)
		for item in project_list:
			#忽略excel配置文件中的空行
			if item != [u'', u'', u'', u''] and item != [u'\u5b9e\u4f8b\u6570\u636e', u'', u'', u'']:
				#print item,type(item)
				#print item[0],type(item[0]),item[1],type(item[1]),item[2],type(item[2]),item[3],type(item[3])
				gitlab_url = host + "/api/v4/projects/" + item[1] + "/jobs/artifacts/" + item[3] + "/download?job=" + get_job_name(item[2])
				#print gitlab_url
				download_project_artifact(gitlab_url,item[2])
				clean(download_dir)     
				clean(unzip_dir)        
				deploy(item[2])
		'''
		gitlab_url = host + "/api/v4/projects/" + sys.argv[1] + "/jobs/artifacts/" + sys.argv[3] + "/download?job=" + get_job_name(sys.argv[2])
		#print gitlab_url
		#定义下载及解压缩目录
		download_dir = download_base_dir.rstrip("/") + "/" + os.path.basename(__file__).split('.')[0] + "-download-" + datetime.date.today().strftime("%Y-%m-%d") + "-" + sys.argv[2]
		unzip_dir = unzip_base_dir.rstrip("/") + "/" + os.path.basename(__file__).split('.')[0] + "-unzip-" + datetime.date.today().strftime("%Y-%m-%d") + "-" + sys.argv[2]
		#下载压缩包及解压备份
		ret = download_project_artifact(gitlab_url,sys.argv[2])
		if ret:
			#清除下载及解压缩临时目录及文件
			clean(download_dir)     
			clean(unzip_dir)        
			#发布服务
			deploy(sys.argv[2])
		else:
			print "\033[41m 项目：%s tag：%s 下载失败 \033[0m" %(item[2],item[3])
			logging.exception("\033[41m 项目：%s tag：%s 下载失败 \033[0m" %(item[2],item[3]))
	except Exception as e:
		print "\033[41m %s \033[0m" %(e)
		logging.exception(e)
	finally:
		print "EOF"
		logging.info("EOF")
