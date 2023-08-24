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

 Date: 18/08/2023 13:19:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

use myweb;
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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_wf_type
-- ----------------------------
INSERT INTO `myapp_wf_type` VALUES (1, '生产发布', '2023-08-02 09:51:24.482499', '2023-08-02 09:51:24.482499');
-- INSERT INTO `myapp_wf_type` VALUES (2, '请假', '2023-08-15 14:43:29.398797', '2023-08-15 14:43:29.398797');
-- INSERT INTO `myapp_wf_type` VALUES (3, '增加监控', '2023-08-15 14:43:54.068585', '2023-08-15 14:43:54.068585');

SET FOREIGN_KEY_CHECKS = 1;
