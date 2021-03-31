create database if not exists `django_test` default character set utf8mb4 collate utf8mb4_general_ci;
grant all on django_test.* to myweb@'%' identified by 'myweb';
flush privileges;
