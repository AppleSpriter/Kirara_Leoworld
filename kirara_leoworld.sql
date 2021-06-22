/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : kirara_leoworld

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2021-06-22 11:52:33
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `achievement`
-- ----------------------------
DROP TABLE IF EXISTS `achievement`;
CREATE TABLE `achievement` (
  `achievementid` varchar(48) NOT NULL,
  `name` varchar(96) NOT NULL,
  `startdate` datetime NOT NULL,
  `enddate` datetime DEFAULT NULL,
  `planinvest` bigint(20) NOT NULL,
  `nowinvest` bigint(20) NOT NULL,
  PRIMARY KEY (`achievementid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of achievement
-- ----------------------------
INSERT INTO `achievement` VALUES ('1', '完成开题报告', '2020-10-19 14:47:56', '2020-10-29 16:37:16', '1680', '1725');
INSERT INTO `achievement` VALUES ('10', '完善数学导图', '2020-10-28 09:32:41', null, '4800', '275');
INSERT INTO `achievement` VALUES ('11', '完成开题 第二期', '2020-10-29 16:38:08', '2020-11-25 16:40:28', '1200', '1000');
INSERT INTO `achievement` VALUES ('12', '立直麻将进阶学习', '2020-10-30 22:54:48', null, '4800', '380');
INSERT INTO `achievement` VALUES ('13', '行政日常', '2020-11-15 14:59:49', null, '6000', '1125');
INSERT INTO `achievement` VALUES ('14', '理解tf 第三期', '2020-11-30 09:26:35', '2021-06-22 11:25:27', '6000', '1050');
INSERT INTO `achievement` VALUES ('15', '论文撰写初级入门', '2021-06-09 15:59:03', null, '3000', '825');
INSERT INTO `achievement` VALUES ('16', 'Blender初级入门', '2021-06-09 16:27:16', null, '3000', '225');
INSERT INTO `achievement` VALUES ('17', '游戏娱乐专业训练', '2021-06-21 11:12:00', null, '24000', '180');
INSERT INTO `achievement` VALUES ('2', '番剧鉴赏进阶学习', '2020-10-19 17:48:07', null, '6000', '910');
INSERT INTO `achievement` VALUES ('3', 'Golang初级入门', '2020-10-19 17:53:24', null, '2400', '175');
INSERT INTO `achievement` VALUES ('4', '写作提升', '2020-10-19 17:56:56', null, '6000', '2150');
INSERT INTO `achievement` VALUES ('5', '理解TF 第二期', '2020-10-19 17:58:46', '2020-11-29 23:02:57', '2400', '2415');
INSERT INTO `achievement` VALUES ('6', '阅读晋升 第二期', '2020-10-19 18:01:48', null, '2000', '1125');
INSERT INTO `achievement` VALUES ('7', '语言同化 第三期', '2020-10-19 18:03:02', null, '4800', '570');
INSERT INTO `achievement` VALUES ('8', '视频娱乐二阶段', '2020-10-19 18:50:22', null, '6000', '2455');
INSERT INTO `achievement` VALUES ('9', 'Coding初级入门', '2020-10-24 15:27:05', null, '2400', '1900');

-- ----------------------------
-- Table structure for `figure`
-- ----------------------------
DROP TABLE IF EXISTS `figure`;
CREATE TABLE `figure` (
  `figureid` varchar(48) NOT NULL,
  `name` varchar(48) NOT NULL,
  `root` varchar(48) DEFAULT NULL,
  `grade` varchar(10) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `weapon` varchar(48) DEFAULT NULL,
  `sound` varchar(48) DEFAULT NULL,
  `skilllevel` int(11) DEFAULT NULL,
  `love` int(11) DEFAULT NULL,
  `eyecolor` varchar(48) DEFAULT NULL,
  `haircolor` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`figureid`),
  KEY `fk_root` (`root`),
  CONSTRAINT `fk_root` FOREIGN KEY (`root`) REFERENCES `work` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of figure
-- ----------------------------
INSERT INTO `figure` VALUES ('1', '高板桐乃', '我的妹妹哪有这么可爱', 'SS', '49', 'none', '竹达彩奈', '8', '174', '蓝绿色', '浅棕色');
INSERT INTO `figure` VALUES ('10', '园田优', '樱trick', 'A', '1', 'none', '井口裕香', '1', '0', '蓝绿色', '橘黄色');
INSERT INTO `figure` VALUES ('11', '栗山未来', '境界的彼方', 'A', '1', 'none', '种田梨沙', '1', '0', '金色', '茶色');
INSERT INTO `figure` VALUES ('2', '岁纳京子', '摇曳百合', 'S', '1', 'none', '大坪由佳', '1', '50', '蓝色', '黄色');
INSERT INTO `figure` VALUES ('3', '五更琉璃', '我的妹妹哪有这么可爱', 'A', '1', 'none', '花泽香菜', '1', '1', '蓝色', '黑色');
INSERT INTO `figure` VALUES ('4', '平泽唯', '轻音少女!', 'S', '1', 'none', '丰崎爱生', '1', '70', '棕色', '棕色');
INSERT INTO `figure` VALUES ('5', '恋冢小梦', 'Comic Girls', 'A', '1', 'none', '本渡枫', '1', '0', '钢蓝色', '黄色');
INSERT INTO `figure` VALUES ('6', '凉风青叶', 'NEW GAME!', 'A', '9', 'none', '高田忧希', '4', '2', '紫色', '浅紫色');
INSERT INTO `figure` VALUES ('7', '八神光', 'NEW GAME!', 'A', '1', 'none', '日笠阳子', '1', '0', '天蓝色', '米黄色');
INSERT INTO `figure` VALUES ('8', '各务原抚子', '摇曳露营△', 'A', '1', 'none', '花守由美里', '1', '0', '天蓝色', '粉色');
INSERT INTO `figure` VALUES ('9', '犬山葵', '摇曳露营△', 'A', '1', 'none', '丰崎爱生', '1', '0', '草绿色', '黄褐色');

-- ----------------------------
-- Table structure for `lottery`
-- ----------------------------
DROP TABLE IF EXISTS `lottery`;
CREATE TABLE `lottery` (
  `lottery_crystal` int(11) NOT NULL DEFAULT '0',
  `check_date` datetime NOT NULL,
  `admission_date` datetime NOT NULL,
  `login_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of lottery
-- ----------------------------
INSERT INTO `lottery` VALUES ('735', '2021-06-16 22:40:50', '2021-06-21 11:09:52', '2021-06-22 11:49:16');

-- ----------------------------
-- Table structure for `work`
-- ----------------------------
DROP TABLE IF EXISTS `work`;
CREATE TABLE `work` (
  `workid` varchar(48) NOT NULL,
  `name` varchar(48) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `company` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`workid`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of work
-- ----------------------------
INSERT INTO `work` VALUES ('1', '摇曳百合', '2011', 'Animation Studio');
INSERT INTO `work` VALUES ('10', '轻音少女!!', '2010', 'Kyoto Animation');
INSERT INTO `work` VALUES ('11', '樱trick', '2014', 'Studio Deen');
INSERT INTO `work` VALUES ('12', '境界的彼方', '2013', 'Kyoto Animation');
INSERT INTO `work` VALUES ('2', '我的妹妹哪有这么可爱', '2010', 'AIC');
INSERT INTO `work` VALUES ('3', '摇曳露营△', '2018', 'C-Station');
INSERT INTO `work` VALUES ('4', 'Comic Girls', '2018', 'Nexus');
INSERT INTO `work` VALUES ('5', 'Slow Start', '2018', 'CloverWorks');
INSERT INTO `work` VALUES ('6', 'NEW GAME!', '2016', 'Animation Studio');
INSERT INTO `work` VALUES ('7', 'NEW GAME!!', '2017', 'Animation Studio');
INSERT INTO `work` VALUES ('8', '街角魔族', '2019', 'J.C.STAFF');
INSERT INTO `work` VALUES ('9', '轻音少女!', '2009', 'Kyoto Animation');
