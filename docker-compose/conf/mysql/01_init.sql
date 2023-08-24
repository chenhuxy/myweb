create database if not exists `django_test` default character set utf8 collate utf8_general_ci;
grant all on myweb.* to myweb@'%' identified by 'myweb';
flush privileges;
