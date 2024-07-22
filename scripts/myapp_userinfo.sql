/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.38.129
 Source Server Type    : MySQL
 Source Server Version : 50742
 Source Host           : 192.168.38.129:3306
 Source Schema         : myweb

 Target Server Type    : MySQL
 Target Server Version : 50742
 File Encoding         : 65001

 Date: 18/07/2024 17:13:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
  `origin` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_userinfo
-- ----------------------------
INSERT INTO `myapp_userinfo` VALUES (1, 'pbkdf2_sha256$120000$JT1Etz13KP5q$kfXVIxSM/LnIJxiO1+ASXb67+9BIBcGjIjjMMK3t8+I=', NULL, 1, 'admin-local', '', '', 'admin@localhost', 1, 1, '2024-07-18 17:12:28.938738', 0, NULL, 'local');

SET FOREIGN_KEY_CHECKS = 1;
