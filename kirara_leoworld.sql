/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : kirara_leowrold_developing

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2021-08-16 13:47:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `adventure`
-- ----------------------------
DROP TABLE IF EXISTS `adventure`;
CREATE TABLE `adventure` (
  `adventureid` int(48) NOT NULL AUTO_INCREMENT,
  `name` varchar(96) NOT NULL,
  `startdate` datetime NOT NULL,
  `enddate` datetime DEFAULT NULL,
  `planinvest` bigint(20) NOT NULL,
  `nowinvest` bigint(20) NOT NULL,
  `lastopendate` datetime NOT NULL,
  PRIMARY KEY (`adventureid`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of adventure
-- ----------------------------
INSERT INTO `adventure` VALUES ('1', '完成开题报告', '2020-10-19 14:47:56', '2020-10-29 16:37:16', '1680', '1725', '2021-06-01 14:49:31');
INSERT INTO `adventure` VALUES ('2', '番剧鉴赏进阶学习', '2020-10-19 17:48:07', null, '6000', '1085', '2021-07-05 20:12:56');
INSERT INTO `adventure` VALUES ('3', 'Golang初级入门', '2020-10-19 17:53:24', null, '2400', '200', '2021-06-01 14:50:10');
INSERT INTO `adventure` VALUES ('4', '写作提升', '2020-10-19 17:56:56', null, '6000', '2390', '2021-07-06 21:46:42');
INSERT INTO `adventure` VALUES ('5', '理解TF 第二期', '2020-10-19 17:58:46', '2020-11-29 23:02:57', '2400', '2415', '2021-06-01 14:50:16');
INSERT INTO `adventure` VALUES ('6', '阅读晋升 第二期', '2020-10-19 18:01:48', null, '2000', '1175', '2021-06-29 19:29:39');
INSERT INTO `adventure` VALUES ('7', '语言同化 第三期', '2020-10-19 18:03:02', null, '4800', '631', '2021-07-04 17:26:34');
INSERT INTO `adventure` VALUES ('8', '视频娱乐二阶段', '2020-10-19 18:50:22', null, '6000', '3057', '2021-07-06 21:38:16');
INSERT INTO `adventure` VALUES ('9', 'Coding初级入门', '2020-10-24 15:27:05', null, '2400', '2222', '2021-08-13 23:12:28');
INSERT INTO `adventure` VALUES ('10', '完善数学导图', '2020-10-28 09:32:41', null, '4800', '275', '2021-06-01 14:49:36');
INSERT INTO `adventure` VALUES ('11', '完成开题 第二期', '2020-10-29 16:38:08', '2020-11-25 16:40:28', '1200', '1000', '2021-06-01 14:49:40');
INSERT INTO `adventure` VALUES ('12', '立直麻将进阶学习', '2020-10-30 22:54:48', null, '4800', '380', '2021-06-01 14:49:51');
INSERT INTO `adventure` VALUES ('13', '行政日常', '2020-11-15 14:59:49', null, '6000', '1250', '2021-06-25 18:05:58');
INSERT INTO `adventure` VALUES ('14', '理解tf 第三期', '2020-11-30 09:26:35', '2021-06-22 11:25:27', '6000', '1050', '2021-06-01 14:49:58');
INSERT INTO `adventure` VALUES ('15', '论文撰写初级入门', '2021-06-09 15:59:03', null, '3000', '1897', '2021-07-06 22:19:08');
INSERT INTO `adventure` VALUES ('16', 'Blender初级入门', '2021-06-09 16:27:16', null, '3000', '256', '2021-08-16 13:33:21');
INSERT INTO `adventure` VALUES ('17', '游戏娱乐专业训练', '2021-06-21 11:12:00', null, '24000', '1144', '2021-08-13 23:31:24');
INSERT INTO `adventure` VALUES ('18', '整理初级入门', '2021-06-28 23:03:07', null, '3000', '100', '2021-07-01 21:20:59');
INSERT INTO `adventure` VALUES ('19', '心理学初级入门', '2021-07-02 19:40:22', null, '3000', '674', '2021-07-06 21:47:10');
INSERT INTO `adventure` VALUES ('20', '音乐鉴赏初级入门', '2021-07-04 20:42:33', null, '2400', '35', '2021-07-05 10:51:51');

-- ----------------------------
-- Table structure for `figure`
-- ----------------------------
DROP TABLE IF EXISTS `figure`;
CREATE TABLE `figure` (
  `figureid` int(48) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `root` varchar(48) DEFAULT NULL,
  `grade` varchar(10) DEFAULT NULL,
  `weapon_type` varchar(48) DEFAULT NULL,
  `feature` varchar(48) DEFAULT NULL,
  `feature_info` varchar(100) DEFAULT NULL,
  `moe` double NOT NULL,
  `yxr` double NOT NULL,
  `intimacy` double NOT NULL,
  `enthusiasm` double NOT NULL,
  `m_coefficient` double NOT NULL,
  `y_coefficient` double NOT NULL,
  `i_coefficient` double NOT NULL,
  `e_coefficient` double NOT NULL,
  `sound` varchar(48) DEFAULT NULL,
  `love` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `eyecolor` varchar(48) DEFAULT NULL,
  `haircolor` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`figureid`),
  KEY `fk_root` (`root`),
  KEY `name` (`name`),
  CONSTRAINT `fk_root` FOREIGN KEY (`root`) REFERENCES `work` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of figure
-- ----------------------------
INSERT INTO `figure` VALUES ('1', '高坂桐乃', '我的妹妹哪有这么可爱', 'S', '键鼠', '亲妹妹', '初始好感度变为二十，幼驯染值被动提高10%', '82', '108', '79', '40', '1.16', '1.21', '1.12', '1.1', '竹达彩奈', '20', '1', '蓝绿色', '浅棕色');
INSERT INTO `figure` VALUES ('2', '岁纳京子', '摇曳百合', 'S', '画具', '热情', '冒险结束后获得10%的水晶加成', '83', '23', '50', '90', '1.15', '1.05', '1.06', '1.19', '大坪由佳', '0', '1', '蓝色', '黄色');
INSERT INTO `figure` VALUES ('3', '五更琉璃', '我的妹妹哪有这么可爱', 'A', '工具', '第二类中二病', '签到奖励增加20%', '70', '33', '50', '92', '1.17', '1.04', '1.16', '1.17', '花泽香菜', '0', '1', '蓝色', '黑色');
INSERT INTO `figure` VALUES ('4', '平泽唯', '轻音少女', 'S', '乐器', '单线程天才', '每日第五次完成番茄钟(大于等于25min)开始获得20%的水晶加成', '100', '66', '91', '100', '1.24', '1.16', '1.12', '1.2', '丰崎爱生', '0', '1', '棕色', '棕色');
INSERT INTO `figure` VALUES ('5', '恋冢小梦', 'Comic Girls', 'A', '画具', '漫画的执念', '武器加成+10%', '70', '41', '51', '96', '1.09', '1.19', '1.1', '1.15', '本渡枫', '0', '1', '钢蓝色', '黄色');
INSERT INTO `figure` VALUES ('6', '凉风青叶', 'NEW GAME', 'S', '键鼠', '专心工作', '提高5%的高品质材料加成', '90', '55', '67', '93', '1.24', '1.17', '1.14', '1.24', '高田忧希', '0', '1', '紫色', '浅紫色');
INSERT INTO `figure` VALUES ('7', '八神光', 'NEW GAME', 'S', '键鼠 画具', '工作狂', '每日早间签到奖励变为原来的3倍', '88', '45', '90', '95', '1.25', '1.11', '1.15', '1.06', '日笠阳子', '0', '1', '天蓝色', '米黄色');
INSERT INTO `figure` VALUES ('8', '各务原抚子', '摇曳露营', 'A', '工具', '天然呆', '萌值被动提高8%', '55', '22', '56', '51', '1.14', '1.15', '1.05', '1.1', '花守由美里', '0', '1', '天蓝色', '粉色');
INSERT INTO `figure` VALUES ('9', '犬山葵', '摇曳露营', 'A', '工具', '自强者', '升阶所需碎片减少5%', '47', '55', '49', '52', '1.15', '1.16', '1.17', '1.04', '丰崎爱生', '0', '1', '草绿色', '黄褐色');
INSERT INTO `figure` VALUES ('10', '栗山未来', '境界的彼方', 'S', '法器', '单纯与幸运', '冒险时间增加10%，水晶奖励减少50%，高品质材料加成25%', '70', '57', '66', '98', '1.17', '1.18', '1.15', '1.06', '种田梨沙', '0', '1', '金色', '茶色');

-- ----------------------------
-- Table structure for `knapsack`
-- ----------------------------
DROP TABLE IF EXISTS `knapsack`;
CREATE TABLE `knapsack` (
  `id` int(11) NOT NULL,
  `name` varchar(48) DEFAULT NULL,
  `number` int(11) unsigned zerofill NOT NULL,
  `type` varchar(48) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of knapsack
-- ----------------------------
INSERT INTO `knapsack` VALUES ('0', '4星强化料', '00000000005', '消耗品');
INSERT INTO `knapsack` VALUES ('1', '3星强化料', '00000000023', '消耗品');
INSERT INTO `knapsack` VALUES ('2', '2星强化料', '00000000031', '消耗品');
INSERT INTO `knapsack` VALUES ('3', '4星角色书', '00000000019', '消耗品');
INSERT INTO `knapsack` VALUES ('4', '3星角色书', '00000000127', '消耗品');
INSERT INTO `knapsack` VALUES ('5', '2星角色书', '00000000107', '消耗品');
INSERT INTO `knapsack` VALUES ('6', '记忆晶元', '00000000000', '兑换材料');

-- ----------------------------
-- Table structure for `log_adventure`
-- ----------------------------
DROP TABLE IF EXISTS `log_adventure`;
CREATE TABLE `log_adventure` (
  `adventure_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) DEFAULT NULL,
  `last_time` int(11) NOT NULL,
  `starttime` datetime NOT NULL,
  `endtime` datetime NOT NULL,
  `crystal_add` int(11) NOT NULL,
  `crystal_hold` int(11) NOT NULL,
  `assistant` varchar(48) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`adventure_id`),
  KEY `FK_advname` (`name`),
  CONSTRAINT `FK_advname` FOREIGN KEY (`name`) REFERENCES `adventure` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of log_adventure
-- ----------------------------
INSERT INTO `log_adventure` VALUES ('1', 'Coding初级入门', '2', '2021-08-13 23:12:16', '2021-08-13 23:12:19', '260', '1459200', null, '');
INSERT INTO `log_adventure` VALUES ('2', 'Coding初级入门', '2', '2021-08-13 23:12:24', '2021-08-13 23:12:28', '260', '1459460', null, '');
INSERT INTO `log_adventure` VALUES ('3', '游戏娱乐专业训练', '2', '2021-08-13 23:31:21', '2021-08-13 23:31:24', '260', '1459720', null, '');
INSERT INTO `log_adventure` VALUES ('4', 'Golang初级入门', '25', '2021-08-16 11:08:58', '2021-08-16 11:09:18', '0', '1459200', null, null);
INSERT INTO `log_adventure` VALUES ('5', '番剧鉴赏进阶学习', '10', '2021-08-16 11:09:38', '2021-08-16 11:09:40', '0', '1459200', null, null);
INSERT INTO `log_adventure` VALUES ('6', '语言同化 第三期', '50', '2021-08-16 11:09:55', '2021-08-16 11:09:57', '0', '1459200', null, null);
INSERT INTO `log_adventure` VALUES ('7', 'Blender初级入门', '3', '2021-08-16 12:04:00', '2021-08-16 12:04:04', '260', '1440700', '', '');
INSERT INTO `log_adventure` VALUES ('8', 'Blender初级入门', '3', '2021-08-16 12:05:06', '2021-08-16 12:05:10', '359', '1441059', '平泽唯', '');
INSERT INTO `log_adventure` VALUES ('9', 'Blender初级入门', '3', '2021-08-16 12:18:30', '2021-08-16 12:18:35', '359', '1441418', '平泽唯', '');
INSERT INTO `log_adventure` VALUES ('10', 'Blender初级入门', '3', '2021-08-16 12:27:36', '2021-08-16 12:27:40', '307', '1441725', '栗山未来', '');
INSERT INTO `log_adventure` VALUES ('11', 'Blender初级入门', '3', '2021-08-16 13:24:22', '2021-08-16 13:24:27', '344', '1444405', '八神光', '');
INSERT INTO `log_adventure` VALUES ('12', 'Blender初级入门', '3', '2021-08-16 13:26:10', '2021-08-16 13:26:15', '344', '1444749', '八神光', '');
INSERT INTO `log_adventure` VALUES ('13', 'Blender初级入门', '3', '2021-08-16 13:29:34', '2021-08-16 13:29:39', '344', '1445093', '八神光', '');
INSERT INTO `log_adventure` VALUES ('14', 'Blender初级入门', '3', '2021-08-16 13:31:34', '2021-08-16 13:31:38', '344', '1445437', '八神光', '');
INSERT INTO `log_adventure` VALUES ('15', 'Blender初级入门', '3', '2021-08-16 13:33:17', '2021-08-16 13:33:21', '344', '1445781', '八神光', '');

-- ----------------------------
-- Table structure for `log_lottery_charc`
-- ----------------------------
DROP TABLE IF EXISTS `log_lottery_charc`;
CREATE TABLE `log_lottery_charc` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `lottery_time` datetime NOT NULL,
  `grade` int(48) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of log_lottery_charc
-- ----------------------------
INSERT INTO `log_lottery_charc` VALUES ('1', '五更琉璃', '2021-08-13 21:23:48', '4');
INSERT INTO `log_lottery_charc` VALUES ('3', '3星角色书3个', '2021-08-13 21:26:33', '3');
INSERT INTO `log_lottery_charc` VALUES ('4', '3星角色书2个', '2021-08-13 21:26:35', '3');
INSERT INTO `log_lottery_charc` VALUES ('5', '各务原抚子', '2021-08-13 21:26:39', '4');
INSERT INTO `log_lottery_charc` VALUES ('6', '犬山葵', '2021-08-13 21:32:35', '4');
INSERT INTO `log_lottery_charc` VALUES ('7', '3星角色书2个', '2021-08-13 21:32:39', '3');
INSERT INTO `log_lottery_charc` VALUES ('8', '各务原抚子', '2021-08-13 21:32:41', '4');
INSERT INTO `log_lottery_charc` VALUES ('9', '2星强化料4个', '2021-08-13 21:32:43', '2');
INSERT INTO `log_lottery_charc` VALUES ('10', '2星角色书3个', '2021-08-13 21:32:44', '2');
INSERT INTO `log_lottery_charc` VALUES ('11', '恋冢小梦', '2021-08-13 21:32:46', '4');
INSERT INTO `log_lottery_charc` VALUES ('12', '2星角色书3个', '2021-08-13 21:37:59', '2');
INSERT INTO `log_lottery_charc` VALUES ('13', '2星角色书2个', '2021-08-13 21:38:02', '2');
INSERT INTO `log_lottery_charc` VALUES ('14', '2星强化料3个', '2021-08-13 21:38:46', '2');
INSERT INTO `log_lottery_charc` VALUES ('15', '五更琉璃', '2021-08-13 21:38:47', '4');
INSERT INTO `log_lottery_charc` VALUES ('16', '五更琉璃', '2021-08-13 21:38:49', '4');
INSERT INTO `log_lottery_charc` VALUES ('17', '五更琉璃', '2021-08-13 21:38:51', '4');
INSERT INTO `log_lottery_charc` VALUES ('18', '4星角色书2个', '2021-08-13 21:39:49', '4');
INSERT INTO `log_lottery_charc` VALUES ('19', '恋冢小梦', '2021-08-13 21:39:51', '4');
INSERT INTO `log_lottery_charc` VALUES ('20', '3星角色书3个', '2021-08-13 21:44:37', '3');
INSERT INTO `log_lottery_charc` VALUES ('21', '2星强化料4个', '2021-08-13 22:21:13', '2');
INSERT INTO `log_lottery_charc` VALUES ('22', '2星角色书3个', '2021-08-13 22:21:17', '2');
INSERT INTO `log_lottery_charc` VALUES ('23', '3星强化料3个', '2021-08-13 22:21:18', '3');
INSERT INTO `log_lottery_charc` VALUES ('24', '3星角色书3个', '2021-08-13 22:21:19', '3');
INSERT INTO `log_lottery_charc` VALUES ('25', '3星角色书2个', '2021-08-13 22:21:21', '3');
INSERT INTO `log_lottery_charc` VALUES ('26', '3星强化料1个', '2021-08-13 22:21:22', '3');
INSERT INTO `log_lottery_charc` VALUES ('27', '3星角色书2个', '2021-08-13 22:21:23', '3');
INSERT INTO `log_lottery_charc` VALUES ('28', '3星角色书2个', '2021-08-13 22:21:24', '3');
INSERT INTO `log_lottery_charc` VALUES ('29', '3星角色书3个', '2021-08-13 22:21:29', '3');
INSERT INTO `log_lottery_charc` VALUES ('30', '3星角色书1个', '2021-08-13 22:21:30', '3');
INSERT INTO `log_lottery_charc` VALUES ('31', '3星角色书2个', '2021-08-13 22:21:31', '3');
INSERT INTO `log_lottery_charc` VALUES ('32', '3星角色书3个', '2021-08-13 22:21:32', '3');
INSERT INTO `log_lottery_charc` VALUES ('33', '3星角色书3个', '2021-08-13 22:21:33', '3');
INSERT INTO `log_lottery_charc` VALUES ('34', '2星角色书5个', '2021-08-13 22:21:34', '2');
INSERT INTO `log_lottery_charc` VALUES ('35', '3星角色书2个', '2021-08-13 22:21:35', '3');
INSERT INTO `log_lottery_charc` VALUES ('36', '3星强化料1个', '2021-08-13 22:21:36', '3');
INSERT INTO `log_lottery_charc` VALUES ('37', '4星角色书1个', '2021-08-13 22:21:37', '4');
INSERT INTO `log_lottery_charc` VALUES ('38', '4星强化料1个', '2021-08-13 22:21:38', '4');
INSERT INTO `log_lottery_charc` VALUES ('39', '3星角色书1个', '2021-08-13 22:21:40', '3');
INSERT INTO `log_lottery_charc` VALUES ('40', '3星角色书3个', '2021-08-13 22:21:40', '3');
INSERT INTO `log_lottery_charc` VALUES ('41', '2星强化料5个', '2021-08-13 22:21:41', '2');
INSERT INTO `log_lottery_charc` VALUES ('42', '2星角色书3个', '2021-08-13 22:21:42', '2');
INSERT INTO `log_lottery_charc` VALUES ('43', '3星角色书2个', '2021-08-13 22:21:43', '3');
INSERT INTO `log_lottery_charc` VALUES ('44', '2星角色书5个', '2021-08-13 22:21:45', '2');
INSERT INTO `log_lottery_charc` VALUES ('45', '2星角色书4个', '2021-08-13 22:21:46', '2');
INSERT INTO `log_lottery_charc` VALUES ('46', '2星角色书5个', '2021-08-13 22:21:48', '2');
INSERT INTO `log_lottery_charc` VALUES ('47', '2星角色书2个', '2021-08-13 22:21:49', '2');
INSERT INTO `log_lottery_charc` VALUES ('48', '3星角色书2个', '2021-08-13 22:21:50', '3');
INSERT INTO `log_lottery_charc` VALUES ('49', '恋冢小梦', '2021-08-13 22:21:51', '4');
INSERT INTO `log_lottery_charc` VALUES ('50', '樱花针管笔', '2021-08-13 22:21:53', '5');
INSERT INTO `log_lottery_charc` VALUES ('51', '3星角色书2个', '2021-08-13 22:22:00', '3');
INSERT INTO `log_lottery_charc` VALUES ('52', '3星角色书3个', '2021-08-13 22:22:20', '3');
INSERT INTO `log_lottery_charc` VALUES ('53', '2星强化料2个', '2021-08-13 22:22:21', '2');
INSERT INTO `log_lottery_charc` VALUES ('54', '凉风青叶', '2021-08-14 14:04:47', '5');
INSERT INTO `log_lottery_charc` VALUES ('55', '2星角色书2个', '2021-08-14 14:07:03', '2');
INSERT INTO `log_lottery_charc` VALUES ('56', '平泽唯', '2021-08-14 14:12:58', '5');
INSERT INTO `log_lottery_charc` VALUES ('57', '栗山未来', '2021-08-14 14:13:04', '5');
INSERT INTO `log_lottery_charc` VALUES ('58', '4星角色书2个', '2021-08-14 14:14:39', '4');
INSERT INTO `log_lottery_charc` VALUES ('59', '凉风青叶', '2021-08-14 14:14:42', '5');
INSERT INTO `log_lottery_charc` VALUES ('60', '凉风青叶', '2021-08-14 19:05:05', '5');
INSERT INTO `log_lottery_charc` VALUES ('61', '2星强化料2个', '2021-08-14 19:05:52', '2');
INSERT INTO `log_lottery_charc` VALUES ('62', '3星角色书2个', '2021-08-14 19:06:09', '3');
INSERT INTO `log_lottery_charc` VALUES ('63', '2星角色书2个', '2021-08-14 19:06:10', '2');
INSERT INTO `log_lottery_charc` VALUES ('64', '3星角色书2个', '2021-08-14 19:06:11', '3');
INSERT INTO `log_lottery_charc` VALUES ('65', '2星角色书5个', '2021-08-14 19:06:12', '2');
INSERT INTO `log_lottery_charc` VALUES ('66', '4星强化料1个', '2021-08-14 19:06:13', '4');
INSERT INTO `log_lottery_charc` VALUES ('67', '4星角色书1个', '2021-08-14 19:06:52', '4');
INSERT INTO `log_lottery_charc` VALUES ('68', '3星角色书1个', '2021-08-14 19:06:54', '3');
INSERT INTO `log_lottery_charc` VALUES ('69', '3星角色书2个', '2021-08-14 19:06:55', '3');
INSERT INTO `log_lottery_charc` VALUES ('70', '3星角色书1个', '2021-08-14 19:06:56', '3');
INSERT INTO `log_lottery_charc` VALUES ('71', '3星角色书2个', '2021-08-14 19:06:57', '3');
INSERT INTO `log_lottery_charc` VALUES ('72', '3星角色书1个', '2021-08-14 19:06:57', '3');
INSERT INTO `log_lottery_charc` VALUES ('73', '3星角色书2个', '2021-08-14 19:06:58', '3');
INSERT INTO `log_lottery_charc` VALUES ('74', '3星角色书3个', '2021-08-14 19:06:59', '3');
INSERT INTO `log_lottery_charc` VALUES ('75', '2星角色书3个', '2021-08-14 19:07:01', '2');
INSERT INTO `log_lottery_charc` VALUES ('76', '3星角色书1个', '2021-08-14 19:07:03', '3');
INSERT INTO `log_lottery_charc` VALUES ('77', '4星角色书2个', '2021-08-14 19:07:39', '4');
INSERT INTO `log_lottery_charc` VALUES ('78', '2星角色书4个', '2021-08-14 19:07:41', '2');
INSERT INTO `log_lottery_charc` VALUES ('79', '3星角色书2个', '2021-08-14 19:07:42', '3');
INSERT INTO `log_lottery_charc` VALUES ('80', '2星角色书5个', '2021-08-14 19:07:43', '2');
INSERT INTO `log_lottery_charc` VALUES ('81', '各务原抚子', '2021-08-14 19:07:44', '4');
INSERT INTO `log_lottery_charc` VALUES ('82', '2星强化料3个', '2021-08-14 19:08:15', '2');
INSERT INTO `log_lottery_charc` VALUES ('83', '3星角色书3个', '2021-08-14 19:08:18', '3');
INSERT INTO `log_lottery_charc` VALUES ('84', '3星角色书2个', '2021-08-14 19:08:28', '3');
INSERT INTO `log_lottery_charc` VALUES ('85', '3星角色书2个', '2021-08-14 19:08:31', '3');
INSERT INTO `log_lottery_charc` VALUES ('86', '商用键盘', '2021-08-14 19:09:07', '4');
INSERT INTO `log_lottery_charc` VALUES ('87', '2星角色书4个', '2021-08-14 19:09:10', '2');
INSERT INTO `log_lottery_charc` VALUES ('88', '3星强化料1个', '2021-08-14 19:09:11', '3');
INSERT INTO `log_lottery_charc` VALUES ('89', '2星角色书3个', '2021-08-14 19:10:41', '2');
INSERT INTO `log_lottery_charc` VALUES ('90', '3星角色书3个', '2021-08-14 19:10:43', '3');
INSERT INTO `log_lottery_charc` VALUES ('91', '2星角色书2个', '2021-08-14 19:10:43', '2');
INSERT INTO `log_lottery_charc` VALUES ('92', '各务原抚子', '2021-08-14 19:10:58', '4');
INSERT INTO `log_lottery_charc` VALUES ('93', '3星角色书1个', '2021-08-14 19:11:00', '3');
INSERT INTO `log_lottery_charc` VALUES ('94', '4星角色书1个', '2021-08-14 19:11:01', '4');
INSERT INTO `log_lottery_charc` VALUES ('95', '3星强化料3个', '2021-08-14 19:33:56', '3');
INSERT INTO `log_lottery_charc` VALUES ('96', '3星角色书3个', '2021-08-14 19:33:57', '3');
INSERT INTO `log_lottery_charc` VALUES ('97', '3星角色书3个', '2021-08-14 19:33:58', '3');
INSERT INTO `log_lottery_charc` VALUES ('98', '3星角色书2个', '2021-08-14 19:33:59', '3');
INSERT INTO `log_lottery_charc` VALUES ('99', '4星角色书1个', '2021-08-14 19:34:00', '4');
INSERT INTO `log_lottery_charc` VALUES ('100', '4星强化料2个', '2021-08-14 19:34:00', '4');
INSERT INTO `log_lottery_charc` VALUES ('101', '4星角色书1个', '2021-08-14 19:34:01', '4');
INSERT INTO `log_lottery_charc` VALUES ('102', '各务原抚子', '2021-08-14 19:34:02', '4');
INSERT INTO `log_lottery_charc` VALUES ('103', '3星角色书2个', '2021-08-14 19:34:03', '3');
INSERT INTO `log_lottery_charc` VALUES ('104', '3星角色书2个', '2021-08-14 19:34:03', '3');
INSERT INTO `log_lottery_charc` VALUES ('105', '黄灯帐篷', '2021-08-14 19:34:04', '5');
INSERT INTO `log_lottery_charc` VALUES ('106', '3星强化料2个', '2021-08-14 19:34:27', '3');
INSERT INTO `log_lottery_charc` VALUES ('107', '3星角色书3个', '2021-08-14 19:45:12', '3');
INSERT INTO `log_lottery_charc` VALUES ('108', '3星角色书2个', '2021-08-14 19:47:16', '3');
INSERT INTO `log_lottery_charc` VALUES ('109', '3星角色书3个', '2021-08-14 19:48:06', '3');
INSERT INTO `log_lottery_charc` VALUES ('110', '3星强化料2个', '2021-08-15 07:53:37', '3');
INSERT INTO `log_lottery_charc` VALUES ('111', '3星角色书3个', '2021-08-15 07:53:39', '3');

-- ----------------------------
-- Table structure for `log_lottery_westi`
-- ----------------------------
DROP TABLE IF EXISTS `log_lottery_westi`;
CREATE TABLE `log_lottery_westi` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `lottery_time` datetime NOT NULL,
  `grade` varchar(48) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of log_lottery_westi
-- ----------------------------

-- ----------------------------
-- Table structure for `lottery`
-- ----------------------------
DROP TABLE IF EXISTS `lottery`;
CREATE TABLE `lottery` (
  `lottery_crystal` int(11) NOT NULL DEFAULT '0',
  `check_date` datetime NOT NULL,
  `admission_date` datetime NOT NULL,
  `login_date` datetime NOT NULL,
  `sum_time` bigint(30) NOT NULL,
  `current_girl` varchar(48) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of lottery
-- ----------------------------
INSERT INTO `lottery` VALUES ('1445781', '2021-08-16 13:13:27', '2021-08-16 11:08:32', '2021-08-16 00:02:37', '22961', '八神光');

-- ----------------------------
-- Table structure for `my_figure`
-- ----------------------------
DROP TABLE IF EXISTS `my_figure`;
CREATE TABLE `my_figure` (
  `my_figure_id` int(11) NOT NULL AUTO_INCREMENT,
  `my_figure_name` varchar(48) NOT NULL,
  `level` int(11) NOT NULL,
  `weapon` int(48) DEFAULT NULL,
  `stigma_up` int(48) DEFAULT NULL,
  `stigma_mid` int(48) DEFAULT NULL,
  `stigma_down` int(48) DEFAULT NULL,
  `love` double DEFAULT NULL,
  `moe` double NOT NULL,
  `yxr` double NOT NULL,
  `intimacy` double NOT NULL,
  `enthusiasm` double NOT NULL,
  `skin` varchar(48) NOT NULL,
  `fragment` int(11) NOT NULL,
  `grade` varchar(48) NOT NULL,
  `exp` int(11) NOT NULL,
  PRIMARY KEY (`my_figure_id`),
  KEY `fk_figure` (`my_figure_name`),
  CONSTRAINT `fk_figure` FOREIGN KEY (`my_figure_name`) REFERENCES `figure` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of my_figure
-- ----------------------------
INSERT INTO `my_figure` VALUES ('1', '平泽唯', '20', null, null, null, null, '0', '100', '66', '91', '100', '平泽唯_服务生', '0', 'SSS', '1');
INSERT INTO `my_figure` VALUES ('2', '栗山未来', '1', null, null, null, null, '0', '70', '57', '66', '98', '栗山未来_默认', '60', 'S', '0');
INSERT INTO `my_figure` VALUES ('3', '八神光', '3', null, null, null, null, '4.3975', '88', '45', '90', '95', '八神光_默认', '0', 'SSS', '0');
INSERT INTO `my_figure` VALUES ('4', '岁纳京子', '1', null, null, null, null, '0', '83', '23', '50', '90', '岁纳京子_默认', '0', 'S', '0');
INSERT INTO `my_figure` VALUES ('5', '犬山葵', '1', null, null, null, null, '0', '47', '55', '49', '52', '犬山葵_默认', '8', 'S', '0');
INSERT INTO `my_figure` VALUES ('6', '五更琉璃', '1', null, null, null, null, '0', '70', '33', '50', '92', '五更琉璃_默认', '90', 'A', '0');
INSERT INTO `my_figure` VALUES ('7', '各务原抚子', '1', null, null, null, null, '0', '55', '22', '56', '51', '各务原抚子_默认', '72', 'A', '0');
INSERT INTO `my_figure` VALUES ('8', '恋冢小梦', '2', null, null, null, null, '0', '70', '41', '51', '96', '恋冢小梦_默认', '6', 'S', '0');
INSERT INTO `my_figure` VALUES ('9', '凉风青叶', '20', null, null, null, null, '0', '90', '55', '67', '93', '凉风青叶_魅魔', '0', 'EX', '26');

-- ----------------------------
-- Table structure for `my_weapon`
-- ----------------------------
DROP TABLE IF EXISTS `my_weapon`;
CREATE TABLE `my_weapon` (
  `my_weapon_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `type` varchar(48) NOT NULL,
  `level` int(11) NOT NULL,
  `moe` double NOT NULL,
  `awaken` int(11) NOT NULL,
  PRIMARY KEY (`my_weapon_id`),
  KEY `FK_weapon_name` (`name`),
  CONSTRAINT `FK_weapon_name` FOREIGN KEY (`name`) REFERENCES `weapon` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of my_weapon
-- ----------------------------
INSERT INTO `my_weapon` VALUES ('1', '樱花针管笔', '画具', '1', '88', '0');
INSERT INTO `my_weapon` VALUES ('2', '蔷薇花开弓', '法器', '1', '81', '0');
INSERT INTO `my_weapon` VALUES ('3', '樱花针管笔', '画具', '1', '88', '0');
INSERT INTO `my_weapon` VALUES ('4', '樱花针管笔', '画具', '1', '88', '0');
INSERT INTO `my_weapon` VALUES ('5', '蔷薇花开弓', '法器', '1', '81', '0');
INSERT INTO `my_weapon` VALUES ('6', '樱花针管笔', '画具', '1', '88', '0');
INSERT INTO `my_weapon` VALUES ('7', '血刃', '法器', '1', '75', '0');
INSERT INTO `my_weapon` VALUES ('8', '蔷薇花开弓', '法器', '1', '81', '0');
INSERT INTO `my_weapon` VALUES ('9', '绣针', '工具', '1', '23', '0');
INSERT INTO `my_weapon` VALUES ('10', '樱花针管笔', '画具', '1', '88', '0');
INSERT INTO `my_weapon` VALUES ('11', '商用键盘', '键盘', '1', '50', '0');
INSERT INTO `my_weapon` VALUES ('12', '黄灯帐篷', '工具', '1', '69', '0');

-- ----------------------------
-- Table structure for `weapon`
-- ----------------------------
DROP TABLE IF EXISTS `weapon`;
CREATE TABLE `weapon` (
  `weapon_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `type` varchar(48) NOT NULL,
  `grade` varchar(48) NOT NULL,
  `moe` double NOT NULL,
  `m_coefficient` double NOT NULL,
  `feature` varchar(48) DEFAULT NULL,
  `feature_info` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`weapon_id`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of weapon
-- ----------------------------
INSERT INTO `weapon` VALUES ('1', '吉太', '乐器', '5', '91', '1.22', '唯爱', '平泽唯装备时，moe值再提高5%');
INSERT INTO `weapon` VALUES ('2', '木响板', '乐器', '4', '52', '0.71', null, null);
INSERT INTO `weapon` VALUES ('3', '樱花针管笔', '画具', '5', '88', '1.19', '易断', '冒险结束后，有20%概率该武器折断，不享受任何加成');
INSERT INTO `weapon` VALUES ('4', '水彩铅', '画具', '4', '42', '0.81', null, null);
INSERT INTO `weapon` VALUES ('5', '商用键盘', '键盘', '4', '50', '0.85', null, null);
INSERT INTO `weapon` VALUES ('6', 'ikbc', '键盘', '5', '88', '1.2', null, null);
INSERT INTO `weapon` VALUES ('7', '绣针', '工具', '4', '23', '0.6', null, null);
INSERT INTO `weapon` VALUES ('8', '黄灯帐篷', '工具', '5', '69', '1.1', null, null);
INSERT INTO `weapon` VALUES ('9', '血刃', '法器', '5', '75', '1.16', '未来之血', '栗山未来装备时，武器萌值全额加成给熟悉值');
INSERT INTO `weapon` VALUES ('10', '蔷薇花开弓', '法器', '5', '81', '1.06', null, null);
INSERT INTO `weapon` VALUES ('11', '黑魔导书', '法器', '4', '0', '1.1', null, null);

-- ----------------------------
-- Table structure for `work`
-- ----------------------------
DROP TABLE IF EXISTS `work`;
CREATE TABLE `work` (
  `workid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(48) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `company` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`workid`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of work
-- ----------------------------
INSERT INTO `work` VALUES ('1', '摇曳百合', '2011', 'Animation Studio');
INSERT INTO `work` VALUES ('2', '我的妹妹哪有这么可爱', '2010', 'AIC');
INSERT INTO `work` VALUES ('3', '摇曳露营', '2018', 'C-Station');
INSERT INTO `work` VALUES ('4', 'Comic Girls', '2018', 'Nexus');
INSERT INTO `work` VALUES ('5', 'Slow Start', '2018', 'CloverWorks');
INSERT INTO `work` VALUES ('6', 'NEW GAME', '2016', 'Animation Studio');
INSERT INTO `work` VALUES ('7', '街角魔族', '2019', 'J.C.STAFF');
INSERT INTO `work` VALUES ('8', '轻音少女', '2009', 'Kyoto Animation');
INSERT INTO `work` VALUES ('9', '樱trick', '2014', 'Studio Deen');
INSERT INTO `work` VALUES ('10', '境界的彼方', '2013', 'Kyoto Animation');
