# myweb

### 一些功能截图：
![image](pictures/dashboard.png)
![image](pictures/登录.jpg)
![image](pictures/注册.jpg)
![image](pictures/用户及权限认证.jpg)
![image](pictures/工单.jpg)
![image](pictures/发布工单.jpg)
![image](pictures/待办工单.jpg)
![image](pictures/应用列表.jpg)
![image](pictures/发布列表.jpg)
![image](pictures/发布日志.jpg)

### 安装方式及步骤：
   
一. Docker安装（推荐方式）

1.启动服务

        docker-compose up -d
 
2.初始化数据库

        执行scripts目录下sql脚本

       
3.启动成功，浏览器访问 ip/cmdb

	用户名：admin

	密码：admin

二. 本地安装：

1.准备环境： 
        centos7.x 
        Python3.5+ 
        MySQL5.7+ 
        Redis3.x+

2.安装python模块

        yum install python-devel -y
        
        python3 -m venv venv
         
        source venv/bin/activate
         
        pip3 install -r requirements/require.txt

	pip3 install uwsgi==2.0.23
          
3.安装MySQL

        yum install mariadb-server -y && systemctl start mariadb
  
4.安装Redis

        yum install redis -y && systemctl start redis

安装nginx

	yum install nginx -y && systemctl start nginx
	配置在 myweb/docker-compose/conf/nginx/default.conf
  
5.修改settings.py中数据库及Redis配置
        
        
6.初始化数据库

	执行scripts目录下sql脚本
  
7.启动celery

        nohup celery worker -A myweb -P solo -l info &
   
8.启动server

        nohup python3 manage.py runserver 0.0.0.0:8000 &  (websocket访问使用，channel集成在runserver中，所以需要启动)

	uwsgi --ini /myweb/apps/uwsgi/uwsgi.ini   (使用uwsgi启动，替代runserver启动，)

	
   
9.启动成功，浏览器访问 nginx  ip/cmdb
	
	用户名：admin

	密码：admin
