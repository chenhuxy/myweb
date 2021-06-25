/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50732
 Source Host           : localhost:3306
 Source Schema         : django_test

 Target Server Type    : MySQL
 Target Server Version : 50732
 File Encoding         : 65001

 Date: 25/06/2021 17:07:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

use django_test;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 105 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_myapp_userinfo_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_myapp_userinfo_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_asset
-- ----------------------------
DROP TABLE IF EXISTS `myapp_asset`;
CREATE TABLE `myapp_asset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `cabinet_order` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `admin_id` int(11) DEFAULT NULL,
  `business_unit_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `device_status_id` int(11) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_asset_admin_id_b746612c_fk_myapp_userinfo_id`(`admin_id`) USING BTREE,
  INDEX `myapp_asset_business_unit_id_8532cb96_fk_myapp_wf_business_id`(`business_unit_id`) USING BTREE,
  INDEX `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id`(`contract_id`) USING BTREE,
  INDEX `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id`(`device_status_id`) USING BTREE,
  INDEX `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id`(`device_type_id`) USING BTREE,
  INDEX `myapp_asset_idc_id_b7038651_fk_myapp_idc_id`(`idc_id`) USING BTREE,
  CONSTRAINT `myapp_asset_admin_id_b746612c_fk_myapp_userinfo_id` FOREIGN KEY (`admin_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_business_unit_id_8532cb96_fk_myapp_wf_business_id` FOREIGN KEY (`business_unit_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `myapp_contract` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id` FOREIGN KEY (`device_status_id`) REFERENCES `myapp_devicestatus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id` FOREIGN KEY (`device_type_id`) REFERENCES `myapp_devicetype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_idc_id_b7038651_fk_myapp_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `myapp_idc` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_asset_tag
-- ----------------------------
DROP TABLE IF EXISTS `myapp_asset_tag`;
CREATE TABLE `myapp_asset_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `myapp_asset_tag_asset_id_tag_id_104cfa4e_uniq`(`asset_id`, `tag_id`) USING BTREE,
  INDEX `myapp_asset_tag_tag_id_8027e1a2_fk_myapp_tag_id`(`tag_id`) USING BTREE,
  CONSTRAINT `myapp_asset_tag_asset_id_c0323b11_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_tag_tag_id_8027e1a2_fk_myapp_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `myapp_tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_contract
-- ----------------------------
DROP TABLE IF EXISTS `myapp_contract`;
CREATE TABLE `myapp_contract`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cost` int(11) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `license_num` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sn`(`sn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_cpu
-- ----------------------------
DROP TABLE IF EXISTS `myapp_cpu`;
CREATE TABLE `myapp_cpu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `core_num` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_devicestatus
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicestatus`;
CREATE TABLE `myapp_devicestatus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_devicetype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicetype`;
CREATE TABLE `myapp_devicetype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_disk
-- ----------------------------
DROP TABLE IF EXISTS `myapp_disk`;
CREATE TABLE `myapp_disk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_handlelog
-- ----------------------------
DROP TABLE IF EXISTS `myapp_handlelog`;
CREATE TABLE `myapp_handlelog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handle_type` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `summary` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `detail` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creater_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userinfo_id`(`creater_id`) USING BTREE,
  CONSTRAINT `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userinfo_id` FOREIGN KEY (`creater_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_idc
-- ----------------------------
DROP TABLE IF EXISTS `myapp_idc`;
CREATE TABLE `myapp_idc`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_display_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `display_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `floor` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_memory
-- ----------------------------
DROP TABLE IF EXISTS `myapp_memory`;
CREATE TABLE `myapp_memory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_memory_server_info_id_36938d15_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_memory_server_info_id_36938d15_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_monitor
-- ----------------------------
DROP TABLE IF EXISTS `myapp_monitor`;
CREATE TABLE `myapp_monitor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_networkdevice
-- ----------------------------
DROP TABLE IF EXISTS `myapp_networkdevice`;
CREATE TABLE `myapp_networkdevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  CONSTRAINT `myapp_networkdevice_asset_id_522ff50d_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_nic
-- ----------------------------
DROP TABLE IF EXISTS `myapp_nic`;
CREATE TABLE `myapp_nic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ipaddr` char(39) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mac` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `netmask` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_scripttype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_scripttype`;
CREATE TABLE `myapp_scripttype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_server
-- ----------------------------
DROP TABLE IF EXISTS `myapp_server`;
CREATE TABLE `myapp_server`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `bios` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hostname`(`hostname`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  INDEX `myapp_server_sn_asset_id_c7a7ab63_idx`(`sn`, `asset_id`) USING BTREE,
  CONSTRAINT `myapp_server_asset_id_b837c205_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_tag
-- ----------------------------
DROP TABLE IF EXISTS `myapp_tag`;
CREATE TABLE `myapp_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userinfo`;
CREATE TABLE `myapp_userinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `workflow_order` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_userinfo_groups
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userinfo_groups`;
CREATE TABLE `myapp_userinfo_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userinfo_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `myapp_userinfo_groups_userinfo_id_group_id_332b93eb_uniq`(`userinfo_id`, `group_id`) USING BTREE,
  INDEX `myapp_userinfo_groups_group_id_2fd9bb25_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `myapp_userinfo_groups_group_id_2fd9bb25_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_userinfo_groups_userinfo_id_1b25c50d_fk_myapp_userinfo_id` FOREIGN KEY (`userinfo_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_userinfo_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userinfo_user_permissions`;
CREATE TABLE `myapp_userinfo_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userinfo_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `myapp_userinfo_user_perm_userinfo_id_permission_i_219ff9fe_uniq`(`userinfo_id`, `permission_id`) USING BTREE,
  INDEX `myapp_userinfo_user__permission_id_db8aa0f3_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `myapp_userinfo_user__permission_id_db8aa0f3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_userinfo_user__userinfo_id_75a6cc6b_fk_myapp_use` FOREIGN KEY (`userinfo_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_business
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business`;
CREATE TABLE `myapp_wf_business`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `proj_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `repo` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `admin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_business_admin_id_43950faf_fk_myapp_userinfo_id`(`admin_id`) USING BTREE,
  CONSTRAINT `myapp_wf_business_admin_id_43950faf_fk_myapp_userinfo_id` FOREIGN KEY (`admin_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_business_approval
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business_approval`;
CREATE TABLE `myapp_wf_business_approval`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_business_id` int(11) NOT NULL,
  `userinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `myapp_wf_business_approv_wf_business_id_userinfo__00d6179b_uniq`(`wf_business_id`, `userinfo_id`) USING BTREE,
  INDEX `myapp_wf_business_ap_userinfo_id_2dabf761_fk_myapp_use`(`userinfo_id`) USING BTREE,
  CONSTRAINT `myapp_wf_business_ap_userinfo_id_2dabf761_fk_myapp_use` FOREIGN KEY (`userinfo_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_business_ap_wf_business_id_c1bd177e_fk_myapp_wf_` FOREIGN KEY (`wf_business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_business_deploy_history
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business_deploy_history`;
CREATE TABLE `myapp_wf_business_deploy_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `proj_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `repo` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `branch` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tag` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `state` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `logs` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `opertator_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_business_de_opertator_id_03157967_fk_myapp_use`(`opertator_id`) USING BTREE,
  CONSTRAINT `myapp_wf_business_de_opertator_id_03157967_fk_myapp_use` FOREIGN KEY (`opertator_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info`;
CREATE TABLE `myapp_wf_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `status` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `next_assignee` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info_process_history
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_process_history`;
CREATE TABLE `myapp_wf_info_process_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `status` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `next_assignee` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `suggest` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `suggest_content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_proces_business_id_4dc1e294_fk_myapp_wf_`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_proces_type_id_06bc9683_fk_myapp_wf_`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_proces_business_id_4dc1e294_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_proces_type_id_06bc9683_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_type
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_type`;
CREATE TABLE `myapp_wf_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
