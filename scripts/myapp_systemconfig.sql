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

 Date: 13/06/2024 19:05:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for myapp_systemconfig
-- ----------------------------
DROP TABLE IF EXISTS `myapp_systemconfig`;
CREATE TABLE `myapp_systemconfig`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `external_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `active_email_subject` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `verify_email_subject` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gitlab_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gitlab_token` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gitlab_job_name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gitlab_job_name_tomcat` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `wf_email_subject` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_email_subject` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_email_receiver` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_dingtalk_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_welink_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_welink_uuid` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `prom_dingtalk_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `prom_welink_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `prom_welink_uuid` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `deploy_dingtalk_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `deploy_welink_url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `deploy_welink_uuid` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ansible_base_dir` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tomcat_project_list` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `grafana_url` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `skywalking_ui_url` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `api_access_timeout` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of myapp_systemconfig
-- ----------------------------
INSERT INTO `myapp_systemconfig` VALUES (1, 'http://192.168.38.129', '【运维发布系统账号激活邮件】', '【运维发布系统找回密码邮件】', 'https://xxxxx', 'glpat-wMMzPzUF4Hqd79f8hxy7111fgsdfgsf', 'build_java', 'build_java_prod', '【运维发布系统流程审批提醒】', '【Skywalking链路监控告警】', '', '', '', '', '', '', '', '', 'https://open.welink.huaweicloud.com/api/werobot/v1/webhook/send?token=c8a5bfca28ac44f2b3360dc8a4c60778&channel=standard', '181778b68d784679ac3d71d5a09fec86', '/etc/ansible', 'aaa,bbbb,ccc', 'https://xxx/grafana/d/aka/be9e3f56-70f9-509c-9efd-be6e2c0b5292?orgId=1&auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZDR05qWnN0dW9RWndDWFlnQ2pTd0NzSHBvMWhzOVRUZkVTb09mWllVLU0ifQ.eyJzdWIiOiJoeS1kZXYtdXNlciIsIm5hbWUiOiJoeS1kZXYtdXNlciIsImlhdCI6MTcxMzQxODQxMywiZXhwIjo0ODY5MDkyMDEzLCJpc3MiOiJodHRwczovL215LXRva2VuLWlzc3VlciIsIm9yZyI6Imh5Iiwicm9sZSI6IlZpZXdlciJ9.8NL2dpKjpUp_MzLzyit-388mCMAo0SzCHLLcFJZ1nrY', 'http://10.13.13.73/?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJoeS1kZXYtdXNlciIsImV4cCI6NDg2NzQ1NTY5MH0.PBvAHjDvY0hrO4cmohB0_NxSfh5mDsER83pJ63_1xCQ', '5000', 'default');

SET FOREIGN_KEY_CHECKS = 1;
