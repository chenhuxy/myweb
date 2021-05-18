/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50732
Source Host           : localhost:3306
Source Database       : django_test

Target Server Type    : MYSQL
Target Server Version : 50732
File Encoding         : 65001

Date: 2021-05-18 12:11:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app01_admininfo
-- ----------------------------
DROP TABLE IF EXISTS `app01_admininfo`;
CREATE TABLE `app01_admininfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `app01_admininfo_user_id_07a516a1_fk_app01_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `app01_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_asset
-- ----------------------------
DROP TABLE IF EXISTS `app01_asset`;
CREATE TABLE `app01_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(256) DEFAULT NULL,
  `cabinet_order` varchar(256) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `memo` longtext,
  `admin_id` int(11) DEFAULT NULL,
  `business_unit_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `device_status_id` int(11) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_asset_admin_id_2aa09adf_fk_app01_userprofile_id` (`admin_id`),
  KEY `app01_asset_business_unit_id_76c39996_fk_app01_businessunit_id` (`business_unit_id`),
  KEY `app01_asset_contract_id_7aa88c0b_fk_app01_contract_id` (`contract_id`),
  KEY `app01_asset_device_status_id_58f83e46_fk_app01_devicestatus_id` (`device_status_id`),
  KEY `app01_asset_device_type_id_80a55b27_fk_app01_devicetype_id` (`device_type_id`),
  KEY `app01_asset_idc_id_61c5dbb7_fk_app01_idc_id` (`idc_id`),
  CONSTRAINT `app01_asset_admin_id_2aa09adf_fk_app01_userprofile_id` FOREIGN KEY (`admin_id`) REFERENCES `app01_userprofile` (`id`),
  CONSTRAINT `app01_asset_business_unit_id_76c39996_fk_app01_businessunit_id` FOREIGN KEY (`business_unit_id`) REFERENCES `app01_businessunit` (`id`),
  CONSTRAINT `app01_asset_contract_id_7aa88c0b_fk_app01_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `app01_contract` (`id`),
  CONSTRAINT `app01_asset_device_status_id_58f83e46_fk_app01_devicestatus_id` FOREIGN KEY (`device_status_id`) REFERENCES `app01_devicestatus` (`id`),
  CONSTRAINT `app01_asset_device_type_id_80a55b27_fk_app01_devicetype_id` FOREIGN KEY (`device_type_id`) REFERENCES `app01_devicetype` (`id`),
  CONSTRAINT `app01_asset_idc_id_61c5dbb7_fk_app01_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `app01_idc` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_asset_tag
-- ----------------------------
DROP TABLE IF EXISTS `app01_asset_tag`;
CREATE TABLE `app01_asset_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app01_asset_tag_asset_id_tag_id_4107b01c_uniq` (`asset_id`,`tag_id`),
  KEY `app01_asset_tag_tag_id_c4c3836b_fk_app01_tag_id` (`tag_id`),
  CONSTRAINT `app01_asset_tag_asset_id_bf3f8817_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`),
  CONSTRAINT `app01_asset_tag_tag_id_c4c3836b_fk_app01_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `app01_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_blog
-- ----------------------------
DROP TABLE IF EXISTS `app01_blog`;
CREATE TABLE `app01_blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_businessunit
-- ----------------------------
DROP TABLE IF EXISTS `app01_businessunit`;
CREATE TABLE `app01_businessunit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `memo` longtext,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `app01_businessunit_contact_id_eb3f037c_fk_app01_userprofile_id` (`contact_id`),
  CONSTRAINT `app01_businessunit_contact_id_eb3f037c_fk_app01_userprofile_id` FOREIGN KEY (`contact_id`) REFERENCES `app01_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_contract
-- ----------------------------
DROP TABLE IF EXISTS `app01_contract`;
CREATE TABLE `app01_contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `name` varchar(256) NOT NULL,
  `cost` int(11) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `license_num` int(11) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sn` (`sn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_cpu
-- ----------------------------
DROP TABLE IF EXISTS `app01_cpu`;
CREATE TABLE `app01_cpu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `core_num` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_cpu_server_info_id_560f0a05_fk_app01_server_id` (`server_info_id`),
  CONSTRAINT `app01_cpu_server_info_id_560f0a05_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_devicestatus
-- ----------------------------
DROP TABLE IF EXISTS `app01_devicestatus`;
CREATE TABLE `app01_devicestatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_devicetype
-- ----------------------------
DROP TABLE IF EXISTS `app01_devicetype`;
CREATE TABLE `app01_devicetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_disk
-- ----------------------------
DROP TABLE IF EXISTS `app01_disk`;
CREATE TABLE `app01_disk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_disk_server_info_id_528e4e73_fk_app01_server_id` (`server_info_id`),
  CONSTRAINT `app01_disk_server_info_id_528e4e73_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_handlelog
-- ----------------------------
DROP TABLE IF EXISTS `app01_handlelog`;
CREATE TABLE `app01_handlelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handle_type` varchar(256) NOT NULL,
  `summary` varchar(256) NOT NULL,
  `detail` longtext NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `memo` longtext NOT NULL,
  `creater_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_handlelog_creater_id_83796dd3_fk_app01_userprofile_id` (`creater_id`),
  CONSTRAINT `app01_handlelog_creater_id_83796dd3_fk_app01_userprofile_id` FOREIGN KEY (`creater_id`) REFERENCES `app01_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_idc
-- ----------------------------
DROP TABLE IF EXISTS `app01_idc`;
CREATE TABLE `app01_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_display_name` varchar(256) NOT NULL,
  `display_name` varchar(256) NOT NULL,
  `floor` int(11) NOT NULL,
  `memo` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_memory
-- ----------------------------
DROP TABLE IF EXISTS `app01_memory`;
CREATE TABLE `app01_memory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_memory_server_info_id_4d5a46ce_fk_app01_server_id` (`server_info_id`),
  CONSTRAINT `app01_memory_server_info_id_4d5a46ce_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_networkdevice
-- ----------------------------
DROP TABLE IF EXISTS `app01_networkdevice`;
CREATE TABLE `app01_networkdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `sn` varchar(256) NOT NULL,
  `manufactory` varchar(256) DEFAULT NULL,
  `model` varchar(256) DEFAULT NULL,
  `memo` longtext NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_id` (`asset_id`),
  CONSTRAINT `app01_networkdevice_asset_id_63ebb91b_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_nic
-- ----------------------------
DROP TABLE IF EXISTS `app01_nic`;
CREATE TABLE `app01_nic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `ipaddr` char(39) NOT NULL,
  `mac` varchar(256) NOT NULL,
  `netmask` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_nic_server_info_id_319e8f34_fk_app01_server_id` (`server_info_id`),
  CONSTRAINT `app01_nic_server_info_id_319e8f34_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_server
-- ----------------------------
DROP TABLE IF EXISTS `app01_server`;
CREATE TABLE `app01_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(128) NOT NULL,
  `sn` varchar(256) NOT NULL,
  `manufactory` varchar(256) DEFAULT NULL,
  `model` varchar(256) DEFAULT NULL,
  `bios` varchar(256) DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `asset_id` (`asset_id`),
  KEY `app01_server_sn_asset_id_d15a4b63_idx` (`sn`,`asset_id`),
  CONSTRAINT `app01_server_asset_id_24640a52_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_tag
-- ----------------------------
DROP TABLE IF EXISTS `app01_tag`;
CREATE TABLE `app01_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app01_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `app01_userprofile`;
CREATE TABLE `app01_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  `mobile` varchar(256) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=257 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monitor_host
-- ----------------------------
DROP TABLE IF EXISTS `monitor_host`;
CREATE TABLE `monitor_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL,
  `hostid` int(11) NOT NULL,
  `createdate` datetime(6) NOT NULL,
  `lastmodified` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_ge_bytearray
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ge_bytearray`;
CREATE TABLE `myapp_act_ge_bytearray` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `bytes` longblob NOT NULL,
  `deployment_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_act_ge_bytearr_deployment_id_id_006f56f6_fk_myapp_act` (`deployment_id_id`),
  CONSTRAINT `myapp_act_ge_bytearr_deployment_id_id_006f56f6_fk_myapp_act` FOREIGN KEY (`deployment_id_id`) REFERENCES `myapp_act_re_deployment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_hi_actinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_actinst`;
CREATE TABLE `myapp_act_hi_actinst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_def_id` varchar(128) NOT NULL,
  `proc_inst_id` varchar(128) NOT NULL,
  `excution_id` varchar(128) NOT NULL,
  `act_id` varchar(128) NOT NULL,
  `task_id` varchar(128) NOT NULL,
  `call_proc_inst_id` varchar(128) NOT NULL,
  `act_name` varchar(128) NOT NULL,
  `act_type` varchar(128) NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `duration` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_hi_attachment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_attachment`;
CREATE TABLE `myapp_act_hi_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `user_id` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` longtext,
  `type` varchar(128) NOT NULL,
  `task_id` varchar(128) NOT NULL,
  `proc_inst_id` varchar(128) NOT NULL,
  `url` varchar(128) NOT NULL,
  `content_id` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_hi_comment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_comment`;
CREATE TABLE `myapp_act_hi_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(128) NOT NULL,
  `time` datetime(6) NOT NULL,
  `user_id` varchar(128) NOT NULL,
  `task_id` varchar(128) NOT NULL,
  `proc_inst_id` varchar(128) NOT NULL,
  `action` varchar(128) NOT NULL,
  `message` varchar(128) NOT NULL,
  `full_msg` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_hi_procinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_procinst`;
CREATE TABLE `myapp_act_hi_procinst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_inst_id` varchar(128) NOT NULL,
  `bussiness_key` varchar(128) NOT NULL,
  `proc_def_id` varchar(128) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `duration` bigint(20) NOT NULL,
  `start_user_id` varchar(128) NOT NULL,
  `start_act_id` varchar(128) NOT NULL,
  `end_act_id` varchar(128) NOT NULL,
  `super_process_instant_id` varchar(128) NOT NULL,
  `delete_reson` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_hi_taskinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_taskinst`;
CREATE TABLE `myapp_act_hi_taskinst` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_inst_id` varchar(128) NOT NULL,
  `bussiness_key` varchar(128) NOT NULL,
  `proc_def_id` varchar(128) NOT NULL,
  `task_def_key` varchar(128) NOT NULL,
  `excution_id` varchar(128) NOT NULL,
  `parent_task_id` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` longtext,
  `owner` varchar(128) NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `claim_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `priority` varchar(128) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `form_key` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_re_deployment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_re_deployment`;
CREATE TABLE `myapp_act_re_deployment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `category` varchar(128) NOT NULL,
  `deploy_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_ru_execution
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ru_execution`;
CREATE TABLE `myapp_act_ru_execution` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `proc_inst_id` varchar(128) NOT NULL,
  `bussiness_key` varchar(128) NOT NULL,
  `parent_id` varchar(128) NOT NULL,
  `proc_def_id` varchar(128) NOT NULL,
  `super_exec` varchar(128) NOT NULL,
  `act_id` varchar(128) NOT NULL,
  `is_active` int(11) NOT NULL,
  `suspension_state` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_act_ru_task
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ru_task`;
CREATE TABLE `myapp_act_ru_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `excution_id` varchar(128) NOT NULL,
  `proc_inst_id` varchar(128) NOT NULL,
  `proc_def_id` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `parent_task_id` varchar(128) NOT NULL,
  `description` longtext,
  `task_def_key` varchar(128) NOT NULL,
  `owner` varchar(128) NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `priority` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `suspension_state` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_admininfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_admininfo`;
CREATE TABLE `myapp_admininfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `myapp_admininfo_user_id_37067bf6_fk_myapp_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_asset
-- ----------------------------
DROP TABLE IF EXISTS `myapp_asset`;
CREATE TABLE `myapp_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(256) DEFAULT NULL,
  `cabinet_order` varchar(256) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `memo` longtext,
  `admin_id` int(11) DEFAULT NULL,
  `business_unit_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `device_status_id` int(11) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_asset_admin_id_b746612c_fk_myapp_userprofile_id` (`admin_id`),
  KEY `myapp_asset_business_unit_id_8532cb96_fk_myapp_businessunit_id` (`business_unit_id`),
  KEY `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id` (`contract_id`),
  KEY `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id` (`device_status_id`),
  KEY `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id` (`device_type_id`),
  KEY `myapp_asset_idc_id_b7038651_fk_myapp_idc_id` (`idc_id`),
  CONSTRAINT `myapp_asset_admin_id_b746612c_fk_myapp_userprofile_id` FOREIGN KEY (`admin_id`) REFERENCES `myapp_userprofile` (`id`),
  CONSTRAINT `myapp_asset_business_unit_id_8532cb96_fk_myapp_businessunit_id` FOREIGN KEY (`business_unit_id`) REFERENCES `myapp_businessunit` (`id`),
  CONSTRAINT `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `myapp_contract` (`id`),
  CONSTRAINT `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id` FOREIGN KEY (`device_status_id`) REFERENCES `myapp_devicestatus` (`id`),
  CONSTRAINT `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id` FOREIGN KEY (`device_type_id`) REFERENCES `myapp_devicetype` (`id`),
  CONSTRAINT `myapp_asset_idc_id_b7038651_fk_myapp_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `myapp_idc` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_asset_tag
-- ----------------------------
DROP TABLE IF EXISTS `myapp_asset_tag`;
CREATE TABLE `myapp_asset_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `myapp_asset_tag_asset_id_tag_id_104cfa4e_uniq` (`asset_id`,`tag_id`),
  KEY `myapp_asset_tag_tag_id_8027e1a2_fk_myapp_tag_id` (`tag_id`),
  CONSTRAINT `myapp_asset_tag_asset_id_c0323b11_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`),
  CONSTRAINT `myapp_asset_tag_tag_id_8027e1a2_fk_myapp_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `myapp_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_blog
-- ----------------------------
DROP TABLE IF EXISTS `myapp_blog`;
CREATE TABLE `myapp_blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_businessunit
-- ----------------------------
DROP TABLE IF EXISTS `myapp_businessunit`;
CREATE TABLE `myapp_businessunit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `memo` longtext,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `myapp_businessunit_contact_id_8ba2eb46_fk_myapp_userprofile_id` (`contact_id`),
  CONSTRAINT `myapp_businessunit_contact_id_8ba2eb46_fk_myapp_userprofile_id` FOREIGN KEY (`contact_id`) REFERENCES `myapp_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_contract
-- ----------------------------
DROP TABLE IF EXISTS `myapp_contract`;
CREATE TABLE `myapp_contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `name` varchar(256) NOT NULL,
  `cost` int(11) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `license_num` int(11) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sn` (`sn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_cpu
-- ----------------------------
DROP TABLE IF EXISTS `myapp_cpu`;
CREATE TABLE `myapp_cpu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `core_num` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id` (`server_info_id`),
  CONSTRAINT `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_devicestatus
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicestatus`;
CREATE TABLE `myapp_devicestatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_devicetype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicetype`;
CREATE TABLE `myapp_devicetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_disk
-- ----------------------------
DROP TABLE IF EXISTS `myapp_disk`;
CREATE TABLE `myapp_disk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id` (`server_info_id`),
  CONSTRAINT `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_handlelog
-- ----------------------------
DROP TABLE IF EXISTS `myapp_handlelog`;
CREATE TABLE `myapp_handlelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handle_type` varchar(256) NOT NULL,
  `summary` varchar(256) NOT NULL,
  `detail` longtext NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `memo` longtext NOT NULL,
  `creater_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userprofile_id` (`creater_id`),
  CONSTRAINT `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userprofile_id` FOREIGN KEY (`creater_id`) REFERENCES `myapp_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_hostinfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_hostinfo`;
CREATE TABLE `myapp_hostinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(200) NOT NULL,
  `ip` char(39) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_idc
-- ----------------------------
DROP TABLE IF EXISTS `myapp_idc`;
CREATE TABLE `myapp_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_display_name` varchar(256) NOT NULL,
  `display_name` varchar(256) NOT NULL,
  `floor` int(11) NOT NULL,
  `memo` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_memory
-- ----------------------------
DROP TABLE IF EXISTS `myapp_memory`;
CREATE TABLE `myapp_memory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_memory_server_info_id_36938d15_fk_myapp_server_id` (`server_info_id`),
  CONSTRAINT `myapp_memory_server_info_id_36938d15_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_networkdevice
-- ----------------------------
DROP TABLE IF EXISTS `myapp_networkdevice`;
CREATE TABLE `myapp_networkdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `sn` varchar(256) NOT NULL,
  `manufactory` varchar(256) DEFAULT NULL,
  `model` varchar(256) DEFAULT NULL,
  `memo` longtext NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_id` (`asset_id`),
  CONSTRAINT `myapp_networkdevice_asset_id_522ff50d_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_nic
-- ----------------------------
DROP TABLE IF EXISTS `myapp_nic`;
CREATE TABLE `myapp_nic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `model` varchar(256) NOT NULL,
  `ipaddr` char(39) NOT NULL,
  `mac` varchar(256) NOT NULL,
  `netmask` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id` (`server_info_id`),
  CONSTRAINT `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_scripttype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_scripttype`;
CREATE TABLE `myapp_scripttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_server
-- ----------------------------
DROP TABLE IF EXISTS `myapp_server`;
CREATE TABLE `myapp_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(128) NOT NULL,
  `sn` varchar(256) NOT NULL,
  `manufactory` varchar(256) DEFAULT NULL,
  `model` varchar(256) DEFAULT NULL,
  `bios` varchar(256) DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `asset_id` (`asset_id`),
  KEY `myapp_server_sn_asset_id_c7a7ab63_idx` (`sn`,`asset_id`),
  CONSTRAINT `myapp_server_asset_id_b837c205_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_tag
-- ----------------------------
DROP TABLE IF EXISTS `myapp_tag`;
CREATE TABLE `myapp_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `memo` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_usergroup
-- ----------------------------
DROP TABLE IF EXISTS `myapp_usergroup`;
CREATE TABLE `myapp_usergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userinfo`;
CREATE TABLE `myapp_userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` varchar(200) NOT NULL,
  `approval` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext,
  `group_id` int(11) NOT NULL,
  `usertype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_userinfo_group_id_0e6a33cb_fk_myapp_usergroup_id` (`group_id`),
  KEY `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id` (`usertype_id`),
  CONSTRAINT `myapp_userinfo_group_id_0e6a33cb_fk_myapp_usergroup_id` FOREIGN KEY (`group_id`) REFERENCES `myapp_usergroup` (`id`),
  CONSTRAINT `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id` FOREIGN KEY (`usertype_id`) REFERENCES `myapp_usertype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userprofile`;
CREATE TABLE `myapp_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  `mobile` varchar(256) NOT NULL,
  `memo` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_usertype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_usertype`;
CREATE TABLE `myapp_usertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_business
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business`;
CREATE TABLE `myapp_wf_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `proj_id` varchar(128) NOT NULL,
  `repo` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `director_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_business_director_id_f057169c_fk_myapp_userinfo_id` (`director_id`),
  KEY `myapp_wf_business_group_id_ad677b25_fk_myapp_usergroup_id` (`group_id`),
  CONSTRAINT `myapp_wf_business_director_id_f057169c_fk_myapp_userinfo_id` FOREIGN KEY (`director_id`) REFERENCES `myapp_userinfo` (`id`),
  CONSTRAINT `myapp_wf_business_group_id_ad677b25_fk_myapp_usergroup_id` FOREIGN KEY (`group_id`) REFERENCES `myapp_usergroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_business_deploy_history
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business_deploy_history`;
CREATE TABLE `myapp_wf_business_deploy_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `proj_id` varchar(128) NOT NULL,
  `repo` varchar(128) NOT NULL,
  `branch` varchar(128) NOT NULL,
  `tag` varchar(128) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `state` varchar(128) NOT NULL,
  `opertator_id` int(11) NOT NULL,
  `logs` longtext,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_business_de_opertator_id_03157967_fk_myapp_use` (`opertator_id`),
  CONSTRAINT `myapp_wf_business_de_opertator_id_03157967_fk_myapp_use` FOREIGN KEY (`opertator_id`) REFERENCES `myapp_userinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49499 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_info
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info`;
CREATE TABLE `myapp_wf_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `sponsor` varchar(128) NOT NULL,
  `content` longtext,
  `status` varchar(128) NOT NULL,
  `flow_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_info_approval_id_9392c362_fk_myapp_userinfo_id` (`approval_id`),
  KEY `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id` (`business_id`),
  KEY `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id` (`type_id`),
  CONSTRAINT `myapp_wf_info_approval_id_9392c362_fk_myapp_userinfo_id` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`),
  CONSTRAINT `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`),
  CONSTRAINT `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_info_history_commit
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_commit`;
CREATE TABLE `myapp_wf_info_history_commit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `sponsor` varchar(128) NOT NULL,
  `content` longtext,
  `status` varchar(128) NOT NULL,
  `flow_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_info_histor_approval_id_5d1dd8c4_fk_myapp_use` (`approval_id`),
  KEY `myapp_wf_info_histor_business_id_743ce714_fk_myapp_wf_` (`business_id`),
  KEY `myapp_wf_info_histor_type_id_2195c4cc_fk_myapp_wf_` (`type_id`),
  CONSTRAINT `myapp_wf_info_histor_approval_id_5d1dd8c4_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`),
  CONSTRAINT `myapp_wf_info_histor_business_id_743ce714_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`),
  CONSTRAINT `myapp_wf_info_histor_type_id_2195c4cc_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_info_history_complete
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_complete`;
CREATE TABLE `myapp_wf_info_history_complete` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `sponsor` varchar(128) NOT NULL,
  `content` longtext,
  `status` varchar(128) NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) NOT NULL,
  `suggest_content` longtext NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_info_histor_business_id_94d5b168_fk_myapp_wf_` (`business_id`),
  KEY `myapp_wf_info_histor_type_id_8f25dba8_fk_myapp_wf_` (`type_id`),
  CONSTRAINT `myapp_wf_info_histor_business_id_94d5b168_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`),
  CONSTRAINT `myapp_wf_info_histor_type_id_8f25dba8_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_info_history_process
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_process`;
CREATE TABLE `myapp_wf_info_history_process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `sponsor` varchar(128) NOT NULL,
  `content` longtext,
  `status` varchar(128) NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) NOT NULL,
  `suggest_content` longtext NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_info_histor_approval_id_447ee8a2_fk_myapp_use` (`approval_id`),
  KEY `myapp_wf_info_histor_business_id_b73011ce_fk_myapp_wf_` (`business_id`),
  KEY `myapp_wf_info_histor_type_id_8573db3a_fk_myapp_wf_` (`type_id`),
  CONSTRAINT `myapp_wf_info_histor_approval_id_447ee8a2_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`),
  CONSTRAINT `myapp_wf_info_histor_business_id_b73011ce_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`),
  CONSTRAINT `myapp_wf_info_histor_type_id_8573db3a_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_info_history_withdraw
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_withdraw`;
CREATE TABLE `myapp_wf_info_history_withdraw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `sponsor` varchar(128) NOT NULL,
  `content` longtext,
  `status` varchar(128) NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) NOT NULL,
  `suggest_content` longtext NOT NULL,
  `assignee` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `myapp_wf_info_histor_approval_id_a4d90ad0_fk_myapp_use` (`approval_id`),
  KEY `myapp_wf_info_histor_business_id_661674aa_fk_myapp_wf_` (`business_id`),
  KEY `myapp_wf_info_histor_type_id_265d212d_fk_myapp_wf_` (`type_id`),
  CONSTRAINT `myapp_wf_info_histor_approval_id_a4d90ad0_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`),
  CONSTRAINT `myapp_wf_info_histor_business_id_661674aa_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`),
  CONSTRAINT `myapp_wf_info_histor_type_id_265d212d_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for myapp_wf_type
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_type`;
CREATE TABLE `myapp_wf_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for upload_normaluser
-- ----------------------------
DROP TABLE IF EXISTS `upload_normaluser`;
CREATE TABLE `upload_normaluser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `headImg` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
