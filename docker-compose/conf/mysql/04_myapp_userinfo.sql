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

 Date: 05/06/2021 23:58:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for myapp_userinfo
-- ----------------------------

use django_test;

DROP TABLE IF EXISTS `myapp_userinfo`;
CREATE TABLE `myapp_userinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `workflow_order` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `memo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `usertype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id`(`usertype_id`) USING BTREE,
  CONSTRAINT `myapp_userinfo_usertype_id_e172d653_fk_myapp_usertype_id` FOREIGN KEY (`usertype_id`) REFERENCES `myapp_usertype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_userinfo
-- ----------------------------
INSERT INTO `myapp_userinfo` VALUES (1, 'admin', 'admin@example.com', '21232f297a57a5a743894a0e4a801fc3', 1, 0, '2021-06-05 14:32:39.686169', '2021-06-05 14:32:39.686169', '', 1);
INSERT INTO `myapp_userinfo` VALUES (2, '张三', '834163059@qq.com', 'c4ca4238a0b923820dcc509a6f75849b', 1, 2, '2021-06-05 14:35:32.105490', '2021-06-05 23:23:14.765007', 'gfhgfd光合积木规划局', 1);
INSERT INTO `myapp_userinfo` VALUES (3, '李四', 'siyezhh@126.com', 'c4ca4238a0b923820dcc509a6f75849b', 1, 5, '2021-06-05 14:36:06.315535', '2021-06-05 23:23:42.675620', '鼓风机工会经费', 1);
INSERT INTO `myapp_userinfo` VALUES (4, '王五', 'chenhu8906@126.com', 'c4ca4238a0b923820dcc509a6f75849b', 1, 8, '2021-06-05 14:36:26.543368', '2021-06-05 23:23:54.740350', '家航空股份', 1);

SET FOREIGN_KEY_CHECKS = 1;
