/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : kirara_leoworld

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2020-10-22 11:23:19
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
INSERT INTO `achievement` VALUES ('1', '完成开题报告', '2020-10-19 14:47:56', null, '1680', '400');
INSERT INTO `achievement` VALUES ('2', '番剧鉴赏', '2020-10-19 17:48:07', null, '6000', '30');
INSERT INTO `achievement` VALUES ('3', '音游入门', '2020-10-19 17:53:24', null, '1800', '0');
INSERT INTO `achievement` VALUES ('4', '写作提升', '2020-10-19 17:56:56', null, '6000', '50');
INSERT INTO `achievement` VALUES ('5', '理解TF 第二期', '2020-10-19 17:58:46', null, '2400', '0');
INSERT INTO `achievement` VALUES ('6', '阅读晋升 第二期', '2020-10-19 18:01:48', null, '2000', '0');
INSERT INTO `achievement` VALUES ('7', '语言同化 第三期', '2020-10-19 18:03:02', null, '4800', '0');
INSERT INTO `achievement` VALUES ('8', '娱乐进阶', '2020-10-19 18:50:22', null, '6000', '0');

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
  `admission_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of lottery
-- ----------------------------
INSERT INTO `lottery` VALUES ('5260', '2020-10-21 22:30:09', '2020-10-22');

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
