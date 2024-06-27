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

 Date: 07/06/2024 16:11:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for myapp_deploytype
-- ----------------------------
DROP TABLE IF EXISTS `myapp_deploytype`;
CREATE TABLE `myapp_deploytype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_deploytype
-- ----------------------------
INSERT INTO `myapp_deploytype` VALUES (1, '发布服务');
INSERT INTO `myapp_deploytype` VALUES (2, '重启服务');

SET FOREIGN_KEY_CHECKS = 1;
