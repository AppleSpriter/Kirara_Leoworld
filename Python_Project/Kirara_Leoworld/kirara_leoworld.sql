/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : kirara_leoworld

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2019-10-07 14:49:37
*/

SET FOREIGN_KEY_CHECKS=0;

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
INSERT INTO `figure` VALUES ('1', '高板桐乃', '我的妹妹哪有这么可爱', 'S', '1', 'none', '竹达彩奈', '1', '50', '蓝绿色', '浅棕色');
INSERT INTO `figure` VALUES ('2', '岁纳京子', '摇曳百合', 'S', '1', 'none', '大坪由佳', '1', '50', '蓝色', '黄色');
INSERT INTO `figure` VALUES ('3', '五更琉璃', '我的妹妹哪有这么可爱', 'A', '1', 'none', '花泽香菜', '1', '1', '蓝色', '黑色');

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
INSERT INTO `work` VALUES ('2', '我的妹妹哪有这么可爱', '2010', 'AIC');
