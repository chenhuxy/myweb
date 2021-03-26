# myweb

一. 本地安装：

1.准备环境：centos7.x Python3.5+ MySQL5.7+ Redis3.x+

2.安装python开发包

  yum install python-devel -y
  
3.安装MySQL

  yum install mariadb -y && systemctl start mariadb
  
4.安装Redis并启动

  yum install redis -y && systemctl start redis
  
5. 修改settings.py中数据库及Redis配置

6. 初始化数据库

  python manage.py makemigrations && python manage.py migrate
  
7. 启动celery

   nohup celery worker -A myweb -P eventlet -l info &
   
8. 启动server

   nohup python manage.py runserver 0.0.0.0:8000 &
   
   启动成功，浏览器访问ip：8000
   
二. Docker安装（待更新。。）

