-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: jimdb
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acl`
--

DROP TABLE IF EXISTS `acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `src_ip` varchar(45) DEFAULT NULL,
  `src_port` int(11) DEFAULT NULL,
  `dst_ip` varchar(45) DEFAULT NULL,
  `dst_port` int(11) DEFAULT NULL,
  `space_id` int(11) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `erp` varchar(50) NOT NULL COMMENT 'erp账号',
  `mail` varchar(50) NOT NULL COMMENT '邮箱',
  `tel` varchar(15) DEFAULT NULL COMMENT '手机号',
  PRIMARY KEY (`erp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alarm_rule`
--

DROP TABLE IF EXISTS `alarm_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarm_rule` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(300) DEFAULT NULL,
  `target_type` tinyint(4) DEFAULT NULL,
  `index_name` varchar(150) DEFAULT NULL,
  `threshold` varchar(3072) DEFAULT NULL,
  `threshold_type` tinyint(3) DEFAULT NULL,
  `durable_time` int(11) DEFAULT NULL,
  `alarm_interval` int(11) DEFAULT NULL,
  `notify_user` varchar(3072) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `created_user` varchar(96) DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  `modified_user` varchar(90) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ap`
--

DROP TABLE IF EXISTS `ap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ap` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `space_id` bigint(20) NOT NULL COMMENT '空间id',
  `domain` varchar(100) DEFAULT NULL COMMENT '域名',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '修改时间',
  `create_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建人',
  `update_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '修改人',
  `status` tinyint(4) NOT NULL COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='ap';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ap_server`
--

DROP TABLE IF EXISTS `ap_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ap_server` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ap_id` bigint(20) NOT NULL COMMENT 'ap主键',
  `server_id` varchar(100) NOT NULL COMMENT '服务器id',
  `ip` varchar(30) NOT NULL COMMENT '服务器ip',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '修改时间',
  `create_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建人',
  `update_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '修改人',
  `status` tinyint(4) NOT NULL COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='ap_server';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `app_id` int(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `name_cn` varchar(50) DEFAULT NULL,
  `leader` varchar(20) DEFAULT NULL,
  `members` varchar(50) DEFAULT NULL,
  `sys_id` int(20) NOT NULL,
  `space_id` int(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `indexOfSysId` (`sys_id`) USING BTREE,
  KEY `indexOfSpaceId` (`space_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `apply`
--

DROP TABLE IF EXISTS `apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apply` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `space_name` varchar(50) NOT NULL COMMENT '空间名称',
  `estimate_size` int(11) DEFAULT NULL COMMENT '预测容量大小',
  `is_autoextend` tinyint(4) DEFAULT NULL COMMENT '是否自动伸缩',
  `apply_reason` varchar(200) NOT NULL COMMENT '申请原因',
  `deadline` datetime NOT NULL COMMENT '合约期',
  `approver` varchar(50) DEFAULT NULL COMMENT '审批人',
  `applicant` varchar(100) NOT NULL COMMENT '申请人',
  `topology_config` varchar(100) DEFAULT NULL COMMENT '副本数配置，规则：机房1,机房2... 含义：主,从,...',
  `sys_id` bigint(20) NOT NULL COMMENT '系统Id',
  `sys_name` varchar(50) NOT NULL COMMENT '系统名称',
  `app_id` bigint(20) DEFAULT NULL COMMENT '应用ID',
  `app_name` varchar(50) DEFAULT NULL COMMENT '应用名称',
  `user_erps` varchar(1000) DEFAULT NULL COMMENT '用户列表',
  `apply_date` datetime NOT NULL COMMENT '申请时间',
  `approval_status` tinyint(4) NOT NULL COMMENT '申请状态0:审核通过1,审核中2审核不通过',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `client_config`
--

DROP TABLE IF EXISTS `client_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_config` (
  `space_id` bigint(20) NOT NULL COMMENT '空间ID',
  `config_id` int(3) NOT NULL COMMENT '配置ID',
  `version` varchar(32) DEFAULT NULL COMMENT '版本',
  `settings` mediumtext COMMENT '客户端设置项(JSON表示)',
  `remark` varchar(255) DEFAULT NULL COMMENT '说明备注',
  PRIMARY KEY (`space_id`,`config_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `create_state`
--

DROP TABLE IF EXISTS `create_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `create_state` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `request_id` varchar(100) DEFAULT NULL,
  `type` int(10) DEFAULT NULL,
  `master_ip` varchar(20) DEFAULT NULL,
  `master_port` int(10) DEFAULT NULL,
  `status` int(10) DEFAULT NULL,
  `message` varchar(2000) DEFAULT NULL,
  `create_by` varchar(20) DEFAULT NULL,
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `update_date` datetime NOT NULL COMMENT '更新时间',
  `update_by` varchar(20) DEFAULT NULL,
  `slaves` int(10) DEFAULT NULL,
  `mem` bigint(20) DEFAULT NULL,
  `zone_id` bigint(10) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `port` int(10) DEFAULT NULL,
  `space_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `request_id` (`request_id`),
  UNIQUE KEY `request_id_2` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deploy`
--

DROP TABLE IF EXISTS `deploy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deploy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` int(11) NOT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '空间ID',
  `tenant_id` varchar(60) NOT NULL COMMENT '租户id',
  `zone_id` bigint(20) NOT NULL COMMENT '机房信息',
  `current_capacity` bigint(20) NOT NULL COMMENT '当前容量',
  `capacity` bigint(20) NOT NULL COMMENT '大小',
  `status` int(11) NOT NULL COMMENT '状态 1:未部署,10:创建redis,30:绑定域名,500:创建客户端配置,1000:部署成功,-1000:部署失败',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_by` varchar(30) DEFAULT NULL COMMENT '修改人',
  `create_by` varchar(30) DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deploy_detail`
--

DROP TABLE IF EXISTS `deploy_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deploy_detail` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `deploy_id` bigint(20) NOT NULL COMMENT '部署ID',
  `deploy_type` int(11) NOT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '空间ID',
  `tenant_id` varchar(60) NOT NULL,
  `shard_id` bigint(20) DEFAULT NULL COMMENT '分片ID',
  `ip` varchar(32) DEFAULT NULL COMMENT '实例ip',
  `port` int(11) DEFAULT NULL COMMENT '实例端口',
  `capacity` bigint(20) NOT NULL COMMENT '大小',
  `buckets_from` int(11) DEFAULT NULL,
  `buckets_to` int(11) DEFAULT NULL,
  `count` int(11) NOT NULL COMMENT '执行次数',
  `status` int(11) NOT NULL COMMENT '状态 1:未部署,10部署中,1000:部署成功,-1000:部署失败',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '修改时间',
  `create_by` varchar(30) DEFAULT NULL COMMENT '创建人',
  `update_by` varchar(30) DEFAULT NULL COMMENT '修改人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `executor`
--

DROP TABLE IF EXISTS `executor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `executor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(50) NOT NULL COMMENT '适配器名称',
  `type` varchar(20) NOT NULL COMMENT '适配器类型',
  `ip` varchar(20) NOT NULL COMMENT '适配器IP',
  `jmx_port` int(11) NOT NULL DEFAULT '7654' COMMENT '适配器JMX端口',
  `description` varchar(500) DEFAULT NULL COMMENT '描述',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `create_by` int(11) NOT NULL DEFAULT '0' COMMENT '创建人',
  `update_time` datetime NOT NULL COMMENT '修改时间',
  `update_by` int(11) NOT NULL DEFAULT '0' COMMENT '修改人',
  `status` int(4) NOT NULL DEFAULT '1' COMMENT '状态(1启用，0停用，-1删除)',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `executor` WRITE;
/*!40000 ALTER TABLE `executor` DISABLE KEYS */;
INSERT INTO `executor` VALUES (1,'192.168.177.88_7656','TASK','192.168.177.88',7654,'test','2016-04-08 21:48:55',0,'2016-04-08 21:48:55',0,1);
/*!40000 ALTER TABLE `executor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host`
--

DROP TABLE IF EXISTS `host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host` (
  `ip` varchar(64) NOT NULL COMMENT 'ip地址',
  `cpu` varchar(128) DEFAULT NULL COMMENT 'cpu信息',
  `disk` int(11) DEFAULT NULL COMMENT '硬盘容量单位G',
  `memory` int(11) DEFAULT NULL COMMENT '内存容量 单位G',
  `os` tinyint(3) DEFAULT NULL COMMENT '操作系统0:windows,1:linux',
  `ethernet` tinyint(1) DEFAULT NULL COMMENT '网卡 0:千兆,1:万兆',
  `zone` varchar(32) DEFAULT NULL COMMENT '机房',
  `agent` tinyint(1) DEFAULT NULL COMMENT '是否部署agent(默认0:否)',
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `modified_date` datetime NOT NULL COMMENT '改修时间',
  `created_user` varchar(30) NOT NULL COMMENT '创建人',
  `modified_user` varchar(30) NOT NULL COMMENT '修改人',
  `switch_ip` varchar(30) DEFAULT NULL COMMENT '交换机ip',
  `remark` varchar(127) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `host` WRITE;
/*!40000 ALTER TABLE `host` DISABLE KEYS */;
INSERT INTO `host` VALUES ('192.168.177.89','24',4096,256,1,1,'test',0,'2016-02-22 18:13:47','2016-02-22 18:13:47','suncmtest','suncmtest','192.168.166.1-192.168.166.2','jimdbtest'),('192.168.169.51','24',4096,256,1,1,'test',0,'2016-02-22 18:13:47','2016-02-22 18:13:47','suncmtest','suncmtest','192.168.166.1-192.168.166.2','jimdbtest');
/*!40000 ALTER TABLE `host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_port`
--

DROP TABLE IF EXISTS `host_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_port` (
  `port` int(11) NOT NULL,
  `host` varchar(64) NOT NULL,
  `used` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`port`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instance`
--

DROP TABLE IF EXISTS `instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance` (
  `ip` varchar(32) NOT NULL,
  `port` int(8) NOT NULL,
  `master_ip` varchar(32) DEFAULT NULL,
  `master_port` int(8) DEFAULT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '空间ID/集群ID',
  `shard_id` bigint(10) NOT NULL COMMENT '分片ID',
  `copy_id` varchar(32) NOT NULL COMMENT '副本标识',
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `modified_date` datetime NOT NULL COMMENT '修改时间',
  `flag` tinyint(4) NOT NULL COMMENT '1: 有效； 2: 无效',
  PRIMARY KEY (`ip`,`port`),
  KEY `shard_id` (`shard_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instance_temp`
--

DROP TABLE IF EXISTS `instance_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance_temp` (
  `ip` varchar(32) NOT NULL,
  `port` int(8) NOT NULL,
  `master_ip` varchar(32) DEFAULT NULL,
  `master_port` int(8) DEFAULT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '空间ID/集群ID',
  `shard_id` bigint(10) DEFAULT NULL COMMENT '分片ID',
  `copy_id` varchar(32) DEFAULT NULL COMMENT '副本标识',
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `modified_date` datetime NOT NULL COMMENT '修改时间',
  `create_id` bigint(20) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ip`,`port`),
  KEY `shard_id` (`shard_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instance_trash`
--

DROP TABLE IF EXISTS `instance_trash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance_trash` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip` varchar(32) NOT NULL,
  `port` int(8) NOT NULL,
  `master_ip` varchar(32) DEFAULT NULL,
  `master_port` int(8) DEFAULT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '空间ID/集群ID',
  `shard_id` bigint(10) NOT NULL COMMENT '分片ID',
  `copy_id` varchar(32) NOT NULL COMMENT '副本标识',
  `created_reason` varchar(255) DEFAULT '' COMMENT '创建原因',
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `created_by` varchar(128) NOT NULL DEFAULT '' COMMENT '创建这条记录的应用名称',
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`) USING HASH
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jim_old_user`
--

DROP TABLE IF EXISTS `jim_old_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jim_old_user` (
  `cluster_id` bigint(20) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `cluster_name` varchar(255) DEFAULT NULL,
  `cluster_desc` varchar(255) DEFAULT NULL,
  `is_mandatory` int(11) DEFAULT NULL,
  `own_dept1` varchar(255) DEFAULT NULL,
  `own_dept2` varchar(255) DEFAULT NULL,
  `user_emails` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jim_old_user_email`
--

DROP TABLE IF EXISTS `jim_old_user_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jim_old_user_email` (
  `emails` varchar(342) DEFAULT NULL,
  `cluster_id` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scale_log`
--

DROP TABLE IF EXISTS `scale_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scale_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `space_id` bigint(20) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` varchar(512) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `snapshot` mediumtext NOT NULL,
  `status` tinyint(4) unsigned zerofill NOT NULL,
  `created_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=594 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scale_state`
--

DROP TABLE IF EXISTS `scale_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scale_state` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `space_id` bigint(20) DEFAULT NULL,
  `state` int(10) DEFAULT NULL,
  `status` int(10) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `master_ip` varchar(20) DEFAULT NULL,
  `master_port` int(10) DEFAULT NULL,
  `message` varchar(2000) DEFAULT NULL,
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `update_date` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scale_task`
--

DROP TABLE IF EXISTS `scale_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scale_task` (
  `space_id` bigint(20) NOT NULL DEFAULT '0',
  `state_id` bigint(20) DEFAULT NULL,
  `created_date` datetime NOT NULL COMMENT '创建时间',
  `async_state` int(10) DEFAULT NULL,
  `request_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`space_id`),
  UNIQUE KEY `request_id` (`request_id`),
  UNIQUE KEY `request_id_2` (`request_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shard`
--

DROP TABLE IF EXISTS `shard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shard` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `space_id` bigint(20) NOT NULL,
  `buckets_from` int(11) NOT NULL,
  `buckets_to` int(11) NOT NULL,
  `flag` tinyint(4) NOT NULL COMMENT '1: 有效，2：无效',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `space`
--

DROP TABLE IF EXISTS `space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `space` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` varchar(45) NOT NULL COMMENT '实例ID',
  `name` varchar(200) NOT NULL COMMENT '空间名称',
  `zone_id` bigint(20) NOT NULL COMMENT '机房id',
  `capacity` bigint(20) NOT NULL COMMENT '容量，KB',
  `is_autoextend` tinyint(4) NOT NULL COMMENT '是否自动伸缩',
  `is_autofailover` tinyint(4) NOT NULL COMMENT '是否自动failover',
  `password` varchar(64) DEFAULT NULL COMMENT '该空间实例连接密码',
  `cluster_type` tinyint(4) NOT NULL COMMENT '集群类型：1:单机，2:集群',
  `created_date` datetime DEFAULT NULL COMMENT '创建时间',
  `modified_date` datetime DEFAULT NULL COMMENT '修改时间',
  `created_user` varchar(30) DEFAULT NULL COMMENT '创建人(谁审批通过就是谁)',
  `modified_user` varchar(30) DEFAULT NULL COMMENT '修改人',
  `is_lock` tinyint(4) DEFAULT NULL,
  `flag` tinyint(4) NOT NULL COMMENT '1: 有效； 2： 无效',
  `status` int(11) NOT NULL COMMENT '状态 0:创建中,100:使用中,200:扩容中,500:创建失败,600:删除中,601:已删除 ,602:删除失败',
  `tenant_id` varchar(100) NOT NULL COMMENT '租户id',
  `remarks` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid_UNIQUE` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `space_alarm_rule`
--

DROP TABLE IF EXISTS `space_alarm_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `space_alarm_rule` (
  `space_id` bigint(20) NOT NULL,
  `alarm_rule_id` bigint(20) NOT NULL,
  `durable_time` int(11) DEFAULT NULL,
  `alarm_interval` int(11) DEFAULT NULL,
  PRIMARY KEY (`space_id`,`alarm_rule_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `space_user`
--

DROP TABLE IF EXISTS `space_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `space_user` (
  `space_id` bigint(20) NOT NULL COMMENT '空间id',
  `erp` varchar(50) NOT NULL COMMENT 'erp账号',
  `role` char(10) NOT NULL COMMENT '角色(0集群管理员,1集群用户)',
  PRIMARY KEY (`space_id`,`erp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sys`
--

DROP TABLE IF EXISTS `sys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys` (
  `id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL COMMENT '系统名称',
  `level` tinyint(3) DEFAULT NULL COMMENT '系统级别',
  `levelDesc` varchar(20) DEFAULT NULL COMMENT '系统级别描述',
  `leader` varchar(20) DEFAULT NULL COMMENT '系统负责人',
  `oneLevelBranch` varchar(200) NOT NULL COMMENT '一级部门',
  `twoLevelBranch` varchar(200) NOT NULL COMMENT '二级部门',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `type` varchar(50) NOT NULL COMMENT '任务类型',
  `refer_id` int(11) DEFAULT NULL COMMENT '关联ID',
  `priority` tinyint(4) NOT NULL DEFAULT '0' COMMENT '优先级',
  `daemons` tinyint(4) NOT NULL DEFAULT '0' COMMENT '守护进程',
  `owner` varchar(50) DEFAULT NULL COMMENT '所有者',
  `url` varchar(1000) DEFAULT NULL COMMENT '链接',
  `cron` varchar(100) DEFAULT NULL COMMENT 'cron表达式',
  `dispatch_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '调度类型',
  `retry` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否重试',
  `retry_count` int(11) NOT NULL DEFAULT '0' COMMENT '重试次数',
  `retry_time` datetime NOT NULL COMMENT '重试时间',
  `exception` varchar(2000) DEFAULT NULL COMMENT '异常',
  `create_by` varchar(30) DEFAULT NULL COMMENT '创建用户',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_by` varchar(30) DEFAULT NULL COMMENT '更新用户',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `status` tinyint(4) NOT NULL COMMENT '任务状态 0:新增;1:派发;2:执行中;3:执行成功;4:失败，不需要重试;5:审核;6:失败,需要重试;',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=342 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topology`
--

DROP TABLE IF EXISTS `topology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology` (
  `space_id` bigint(20) NOT NULL COMMENT '空间ID',
  `epoch` int(15) DEFAULT NULL COMMENT '配置纪元，配置更新次数',
  `current_topology` mediumtext COMMENT '当前元数据配置',
  `temp_topology` mediumtext COMMENT '临时元数据',
  `token` varchar(64) DEFAULT NULL COMMENT '客户端连接凭证',
  `is_locked` tinyint(4) DEFAULT NULL,
  `locked_date` datetime DEFAULT NULL,
  `locked_by` varchar(128) DEFAULT '',
  PRIMARY KEY (`space_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `erp` varchar(50) NOT NULL COMMENT 'erp账号',
  `department1` varchar(50) DEFAULT NULL COMMENT '一级部门',
  `department2` varchar(50) DEFAULT NULL COMMENT '二级部门',
  `tel` varchar(30) DEFAULT NULL COMMENT '用户电话',
  `mail` varchar(50) DEFAULT NULL COMMENT '用户邮箱',
  `created_date` datetime DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`erp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zone`
--

DROP TABLE IF EXISTS `zone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zone` (
  `id` bigint(20) NOT NULL,
  `code` varchar(50) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL,
  `update_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  `update_by` bigint(20) NOT NULL DEFAULT '0',
  `create_by` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-31 14:23:20
