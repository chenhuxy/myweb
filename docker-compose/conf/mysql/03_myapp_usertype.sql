/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : django_test

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 06/06/2021 00:03:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for myapp_usertype
-- ----------------------------

use django_test;

DROP TABLE IF EXISTS `myapp_usertype`;
CREATE TABLE `myapp_usertype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_usertype
-- ----------------------------
INSERT INTO `myapp_usertype` VALUES (1, 'user', '2021-06-05 14:32:31.163577', '2021-06-05 14:32:31.163577');
INSERT INTO `myapp_usertype` VALUES (2, '管理员', '2021-06-05 23:25:05.780088', '2021-06-05 23:25:19.082790');

SET FOREIGN_KEY_CHECKS = 1;
