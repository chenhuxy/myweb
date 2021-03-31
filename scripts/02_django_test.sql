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

 Date: 31/03/2021 09:19:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

use django_test

-- ----------------------------
-- Table structure for app01_admininfo
-- ----------------------------
DROP TABLE IF EXISTS `app01_admininfo`;
CREATE TABLE `app01_admininfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `app01_admininfo_user_id_07a516a1_fk_app01_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `app01_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_asset
-- ----------------------------
DROP TABLE IF EXISTS `app01_asset`;
CREATE TABLE `app01_asset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cabinet_order` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `admin_id` int(11) DEFAULT NULL,
  `business_unit_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `device_status_id` int(11) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_asset_admin_id_2aa09adf_fk_app01_userprofile_id`(`admin_id`) USING BTREE,
  INDEX `app01_asset_business_unit_id_76c39996_fk_app01_businessunit_id`(`business_unit_id`) USING BTREE,
  INDEX `app01_asset_contract_id_7aa88c0b_fk_app01_contract_id`(`contract_id`) USING BTREE,
  INDEX `app01_asset_device_status_id_58f83e46_fk_app01_devicestatus_id`(`device_status_id`) USING BTREE,
  INDEX `app01_asset_device_type_id_80a55b27_fk_app01_devicetype_id`(`device_type_id`) USING BTREE,
  INDEX `app01_asset_idc_id_61c5dbb7_fk_app01_idc_id`(`idc_id`) USING BTREE,
  CONSTRAINT `app01_asset_admin_id_2aa09adf_fk_app01_userprofile_id` FOREIGN KEY (`admin_id`) REFERENCES `app01_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_business_unit_id_76c39996_fk_app01_businessunit_id` FOREIGN KEY (`business_unit_id`) REFERENCES `app01_businessunit` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_contract_id_7aa88c0b_fk_app01_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `app01_contract` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_device_status_id_58f83e46_fk_app01_devicestatus_id` FOREIGN KEY (`device_status_id`) REFERENCES `app01_devicestatus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_device_type_id_80a55b27_fk_app01_devicetype_id` FOREIGN KEY (`device_type_id`) REFERENCES `app01_devicetype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_idc_id_61c5dbb7_fk_app01_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `app01_idc` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_asset_tag
-- ----------------------------
DROP TABLE IF EXISTS `app01_asset_tag`;
CREATE TABLE `app01_asset_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `app01_asset_tag_asset_id_tag_id_4107b01c_uniq`(`asset_id`, `tag_id`) USING BTREE,
  INDEX `app01_asset_tag_tag_id_c4c3836b_fk_app01_tag_id`(`tag_id`) USING BTREE,
  CONSTRAINT `app01_asset_tag_asset_id_bf3f8817_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_asset_tag_tag_id_c4c3836b_fk_app01_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `app01_tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_blog
-- ----------------------------
DROP TABLE IF EXISTS `app01_blog`;
CREATE TABLE `app01_blog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_businessunit
-- ----------------------------
DROP TABLE IF EXISTS `app01_businessunit`;
CREATE TABLE `app01_businessunit`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `app01_businessunit_contact_id_eb3f037c_fk_app01_userprofile_id`(`contact_id`) USING BTREE,
  CONSTRAINT `app01_businessunit_contact_id_eb3f037c_fk_app01_userprofile_id` FOREIGN KEY (`contact_id`) REFERENCES `app01_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_contract
-- ----------------------------
DROP TABLE IF EXISTS `app01_contract`;
CREATE TABLE `app01_contract`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cost` int(11) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `license_num` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sn`(`sn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_cpu
-- ----------------------------
DROP TABLE IF EXISTS `app01_cpu`;
CREATE TABLE `app01_cpu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `core_num` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_cpu_server_info_id_560f0a05_fk_app01_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `app01_cpu_server_info_id_560f0a05_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_devicestatus
-- ----------------------------
DROP TABLE IF EXISTS `app01_devicestatus`;
CREATE TABLE `app01_devicestatus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_devicetype
-- ----------------------------
DROP TABLE IF EXISTS `app01_devicetype`;
CREATE TABLE `app01_devicetype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_disk
-- ----------------------------
DROP TABLE IF EXISTS `app01_disk`;
CREATE TABLE `app01_disk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_disk_server_info_id_528e4e73_fk_app01_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `app01_disk_server_info_id_528e4e73_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_handlelog
-- ----------------------------
DROP TABLE IF EXISTS `app01_handlelog`;
CREATE TABLE `app01_handlelog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handle_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `summary` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `detail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `creater_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_handlelog_creater_id_83796dd3_fk_app01_userprofile_id`(`creater_id`) USING BTREE,
  CONSTRAINT `app01_handlelog_creater_id_83796dd3_fk_app01_userprofile_id` FOREIGN KEY (`creater_id`) REFERENCES `app01_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_idc
-- ----------------------------
DROP TABLE IF EXISTS `app01_idc`;
CREATE TABLE `app01_idc`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_display_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `display_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `floor` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_memory
-- ----------------------------
DROP TABLE IF EXISTS `app01_memory`;
CREATE TABLE `app01_memory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_memory_server_info_id_4d5a46ce_fk_app01_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `app01_memory_server_info_id_4d5a46ce_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_networkdevice
-- ----------------------------
DROP TABLE IF EXISTS `app01_networkdevice`;
CREATE TABLE `app01_networkdevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  CONSTRAINT `app01_networkdevice_asset_id_63ebb91b_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_nic
-- ----------------------------
DROP TABLE IF EXISTS `app01_nic`;
CREATE TABLE `app01_nic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ipaddr` char(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mac` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `netmask` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app01_nic_server_info_id_319e8f34_fk_app01_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `app01_nic_server_info_id_319e8f34_fk_app01_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `app01_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_server
-- ----------------------------
DROP TABLE IF EXISTS `app01_server`;
CREATE TABLE `app01_server`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bios` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hostname`(`hostname`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  INDEX `app01_server_sn_asset_id_d15a4b63_idx`(`sn`, `asset_id`) USING BTREE,
  CONSTRAINT `app01_server_asset_id_24640a52_fk_app01_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `app01_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_tag
-- ----------------------------
DROP TABLE IF EXISTS `app01_tag`;
CREATE TABLE `app01_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for app01_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `app01_userprofile`;
CREATE TABLE `app01_userprofile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mobile` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 245 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 62 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for monitor_host
-- ----------------------------
DROP TABLE IF EXISTS `monitor_host`;
CREATE TABLE `monitor_host`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hostid` int(11) NOT NULL,
  `createdate` datetime(6) NOT NULL,
  `lastmodified` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_ge_bytearray
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ge_bytearray`;
CREATE TABLE `myapp_act_ge_bytearray`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bytes` longblob NOT NULL,
  `deployment_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_act_ge_bytearr_deployment_id_id_006f56f6_fk_myapp_act`(`deployment_id_id`) USING BTREE,
  CONSTRAINT `myapp_act_ge_bytearr_deployment_id_id_006f56f6_fk_myapp_act` FOREIGN KEY (`deployment_id_id`) REFERENCES `myapp_act_re_deployment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_hi_actinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_actinst`;
CREATE TABLE `myapp_act_hi_actinst`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_def_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `excution_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `act_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `call_proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `act_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `act_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `duration` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_hi_attachment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_attachment`;
CREATE TABLE `myapp_act_hi_attachment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_hi_comment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_comment`;
CREATE TABLE `myapp_act_hi_comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `time` datetime(6) NOT NULL,
  `user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `message` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `full_msg` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_hi_procinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_procinst`;
CREATE TABLE `myapp_act_hi_procinst`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bussiness_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_def_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `duration` bigint(20) NOT NULL,
  `start_user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_act_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `end_act_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `super_process_instant_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `delete_reson` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_hi_taskinst
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_hi_taskinst`;
CREATE TABLE `myapp_act_hi_taskinst`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bussiness_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_def_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_def_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `excution_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `parent_task_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `owner` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `claim_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `priority` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `form_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_re_deployment
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_re_deployment`;
CREATE TABLE `myapp_act_re_deployment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `category` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `deploy_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_ru_execution
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ru_execution`;
CREATE TABLE `myapp_act_ru_execution`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bussiness_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `parent_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_def_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `super_exec` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `act_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_active` int(11) NOT NULL,
  `suspension_state` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_act_ru_task
-- ----------------------------
DROP TABLE IF EXISTS `myapp_act_ru_task`;
CREATE TABLE `myapp_act_ru_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` int(11) NOT NULL,
  `excution_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_inst_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `proc_def_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `parent_task_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `task_def_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `owner` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `priority` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `suspension_state` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_admininfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_admininfo`;
CREATE TABLE `myapp_admininfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `myapp_admininfo_user_id_37067bf6_fk_myapp_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_asset
-- ----------------------------
DROP TABLE IF EXISTS `myapp_asset`;
CREATE TABLE `myapp_asset`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cabinet_num` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cabinet_order` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `admin_id` int(11) DEFAULT NULL,
  `business_unit_id` int(11) DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `device_status_id` int(11) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_asset_admin_id_b746612c_fk_myapp_userprofile_id`(`admin_id`) USING BTREE,
  INDEX `myapp_asset_business_unit_id_8532cb96_fk_myapp_businessunit_id`(`business_unit_id`) USING BTREE,
  INDEX `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id`(`contract_id`) USING BTREE,
  INDEX `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id`(`device_status_id`) USING BTREE,
  INDEX `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id`(`device_type_id`) USING BTREE,
  INDEX `myapp_asset_idc_id_b7038651_fk_myapp_idc_id`(`idc_id`) USING BTREE,
  CONSTRAINT `myapp_asset_admin_id_b746612c_fk_myapp_userprofile_id` FOREIGN KEY (`admin_id`) REFERENCES `myapp_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_business_unit_id_8532cb96_fk_myapp_businessunit_id` FOREIGN KEY (`business_unit_id`) REFERENCES `myapp_businessunit` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_contract_id_9ddba0c9_fk_myapp_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `myapp_contract` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_device_status_id_e9408f27_fk_myapp_devicestatus_id` FOREIGN KEY (`device_status_id`) REFERENCES `myapp_devicestatus` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_device_type_id_a393702f_fk_myapp_devicetype_id` FOREIGN KEY (`device_type_id`) REFERENCES `myapp_devicetype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_asset_idc_id_b7038651_fk_myapp_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `myapp_idc` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_blog
-- ----------------------------
DROP TABLE IF EXISTS `myapp_blog`;
CREATE TABLE `myapp_blog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_businessunit
-- ----------------------------
DROP TABLE IF EXISTS `myapp_businessunit`;
CREATE TABLE `myapp_businessunit`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `myapp_businessunit_contact_id_8ba2eb46_fk_myapp_userprofile_id`(`contact_id`) USING BTREE,
  CONSTRAINT `myapp_businessunit_contact_id_8ba2eb46_fk_myapp_userprofile_id` FOREIGN KEY (`contact_id`) REFERENCES `myapp_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_contract
-- ----------------------------
DROP TABLE IF EXISTS `myapp_contract`;
CREATE TABLE `myapp_contract`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cost` int(11) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `license_num` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sn`(`sn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_cpu
-- ----------------------------
DROP TABLE IF EXISTS `myapp_cpu`;
CREATE TABLE `myapp_cpu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `core_num` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_cpu_server_info_id_fad6a00d_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_devicestatus
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicestatus`;
CREATE TABLE `myapp_devicestatus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_devicetype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_devicetype`;
CREATE TABLE `myapp_devicetype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_disk
-- ----------------------------
DROP TABLE IF EXISTS `myapp_disk`;
CREATE TABLE `myapp_disk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_disk_server_info_id_993d95c9_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_handlelog
-- ----------------------------
DROP TABLE IF EXISTS `myapp_handlelog`;
CREATE TABLE `myapp_handlelog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handle_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `summary` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `detail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `creater_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userprofile_id`(`creater_id`) USING BTREE,
  CONSTRAINT `myapp_handlelog_creater_id_4b8578b3_fk_myapp_userprofile_id` FOREIGN KEY (`creater_id`) REFERENCES `myapp_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_idc
-- ----------------------------
DROP TABLE IF EXISTS `myapp_idc`;
CREATE TABLE `myapp_idc`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_display_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `display_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `floor` int(11) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_memory
-- ----------------------------
DROP TABLE IF EXISTS `myapp_memory`;
CREATE TABLE `myapp_memory`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` double NOT NULL,
  `ifac_type` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_memory_server_info_id_36938d15_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_memory_server_info_id_36938d15_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_networkdevice
-- ----------------------------
DROP TABLE IF EXISTS `myapp_networkdevice`;
CREATE TABLE `myapp_networkdevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  CONSTRAINT `myapp_networkdevice_asset_id_522ff50d_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_nic
-- ----------------------------
DROP TABLE IF EXISTS `myapp_nic`;
CREATE TABLE `myapp_nic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ipaddr` char(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mac` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `netmask` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `server_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id`(`server_info_id`) USING BTREE,
  CONSTRAINT `myapp_nic_server_info_id_5fa06d78_fk_myapp_server_id` FOREIGN KEY (`server_info_id`) REFERENCES `myapp_server` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_server
-- ----------------------------
DROP TABLE IF EXISTS `myapp_server`;
CREATE TABLE `myapp_server`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sn` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `manufactory` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `model` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bios` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `asset_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hostname`(`hostname`) USING BTREE,
  UNIQUE INDEX `asset_id`(`asset_id`) USING BTREE,
  INDEX `myapp_server_sn_asset_id_c7a7ab63_idx`(`sn`, `asset_id`) USING BTREE,
  CONSTRAINT `myapp_server_asset_id_b837c205_fk_myapp_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `myapp_asset` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_tag
-- ----------------------------
DROP TABLE IF EXISTS `myapp_tag`;
CREATE TABLE `myapp_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_usergroup
-- ----------------------------
DROP TABLE IF EXISTS `myapp_usergroup`;
CREATE TABLE `myapp_usergroup`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userinfo`;
CREATE TABLE `myapp_userinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `approval` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `group_id` int(11) NOT NULL,
  `usertype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_userinfo_group_id_0e6a33cb_fk_myapp_usergroup_id`(`group_id`) USING BTREE,
  INDEX `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id`(`usertype_id`) USING BTREE,
  CONSTRAINT `myapp_userinfo_group_id_0e6a33cb_fk_myapp_usergroup_id` FOREIGN KEY (`group_id`) REFERENCES `myapp_usergroup` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id` FOREIGN KEY (`usertype_id`) REFERENCES `myapp_usertype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `myapp_userprofile`;
CREATE TABLE `myapp_userprofile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mobile` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_usertype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_usertype`;
CREATE TABLE `myapp_usertype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_business
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_business`;
CREATE TABLE `myapp_wf_business`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `director_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_business_director_id_f057169c_fk_myapp_userinfo_id`(`director_id`) USING BTREE,
  INDEX `myapp_wf_business_group_id_ad677b25_fk_myapp_usergroup_id`(`group_id`) USING BTREE,
  CONSTRAINT `myapp_wf_business_director_id_f057169c_fk_myapp_userinfo_id` FOREIGN KEY (`director_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_business_group_id_ad677b25_fk_myapp_usergroup_id` FOREIGN KEY (`group_id`) REFERENCES `myapp_usergroup` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info`;
CREATE TABLE `myapp_wf_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `status` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_approval_id_9392c362_fk_myapp_userinfo_id`(`approval_id`) USING BTREE,
  INDEX `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_approval_id_9392c362_fk_myapp_userinfo_id` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_business_id_b1f502e4_fk_myapp_wf_business_id` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_type_id_c6ebb0c0_fk_myapp_wf_type_id` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info_history_commit
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_commit`;
CREATE TABLE `myapp_wf_info_history_commit`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `status` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_histor_approval_id_5d1dd8c4_fk_myapp_use`(`approval_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_business_id_743ce714_fk_myapp_wf_`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_type_id_2195c4cc_fk_myapp_wf_`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_histor_approval_id_5d1dd8c4_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_business_id_743ce714_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_type_id_2195c4cc_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info_history_complete
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_complete`;
CREATE TABLE `myapp_wf_info_history_complete`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `status` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `suggest_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_histor_business_id_94d5b168_fk_myapp_wf_`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_type_id_8f25dba8_fk_myapp_wf_`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_histor_business_id_94d5b168_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_type_id_8f25dba8_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info_history_process
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_process`;
CREATE TABLE `myapp_wf_info_history_process`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `status` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `suggest_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_histor_approval_id_447ee8a2_fk_myapp_use`(`approval_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_business_id_b73011ce_fk_myapp_wf_`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_type_id_8573db3a_fk_myapp_wf_`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_histor_approval_id_447ee8a2_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_business_id_b73011ce_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_type_id_8573db3a_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_info_history_withdraw
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_info_history_withdraw`;
CREATE TABLE `myapp_wf_info_history_withdraw`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sponsor` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `status` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `flow_id` int(11) NOT NULL,
  `suggest` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `suggest_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `assignee` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `finish_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `approval_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_wf_info_histor_approval_id_a4d90ad0_fk_myapp_use`(`approval_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_business_id_661674aa_fk_myapp_wf_`(`business_id`) USING BTREE,
  INDEX `myapp_wf_info_histor_type_id_265d212d_fk_myapp_wf_`(`type_id`) USING BTREE,
  CONSTRAINT `myapp_wf_info_histor_approval_id_a4d90ad0_fk_myapp_use` FOREIGN KEY (`approval_id`) REFERENCES `myapp_userinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_business_id_661674aa_fk_myapp_wf_` FOREIGN KEY (`business_id`) REFERENCES `myapp_wf_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `myapp_wf_info_histor_type_id_265d212d_fk_myapp_wf_` FOREIGN KEY (`type_id`) REFERENCES `myapp_wf_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for myapp_wf_type
-- ----------------------------
DROP TABLE IF EXISTS `myapp_wf_type`;
CREATE TABLE `myapp_wf_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for upload_normaluser
-- ----------------------------
DROP TABLE IF EXISTS `upload_normaluser`;
CREATE TABLE `upload_normaluser`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `headImg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
