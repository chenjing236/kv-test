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
  `erp` varchar(50) NOT NULL COMMENT 'erp�˺�',
  `mail` varchar(50) NOT NULL COMMENT '����',
  `tel` varchar(15) DEFAULT NULL COMMENT '�ֻ���',
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����',
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�id',
  `domain` varchar(100) DEFAULT NULL COMMENT '����',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `update_time` datetime NOT NULL COMMENT '�޸�ʱ��',
  `create_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '������',
  `update_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '�޸���',
  `status` tinyint(4) NOT NULL COMMENT '״̬',
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����',
  `ap_id` bigint(20) NOT NULL COMMENT 'ap����',
  `server_id` varchar(100) NOT NULL COMMENT '������id',
  `ip` varchar(30) NOT NULL COMMENT '������ip',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `update_time` datetime NOT NULL COMMENT '�޸�ʱ��',
  `create_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '������',
  `update_by` bigint(20) NOT NULL DEFAULT '0' COMMENT '�޸���',
  `status` tinyint(4) NOT NULL COMMENT '״̬',
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
  `space_name` varchar(50) NOT NULL COMMENT '�ռ�����',
  `estimate_size` int(11) DEFAULT NULL COMMENT 'Ԥ��������С',
  `is_autoextend` tinyint(4) DEFAULT NULL COMMENT '�Ƿ��Զ�����',
  `apply_reason` varchar(200) NOT NULL COMMENT '����ԭ��',
  `deadline` datetime NOT NULL COMMENT '��Լ��',
  `approver` varchar(50) DEFAULT NULL COMMENT '������',
  `applicant` varchar(100) NOT NULL COMMENT '������',
  `topology_config` varchar(100) DEFAULT NULL COMMENT '���������ã����򣺻���1,����2... ���壺��,��,...',
  `sys_id` bigint(20) NOT NULL COMMENT 'ϵͳId',
  `sys_name` varchar(50) NOT NULL COMMENT 'ϵͳ����',
  `app_id` bigint(20) DEFAULT NULL COMMENT 'Ӧ��ID',
  `app_name` varchar(50) DEFAULT NULL COMMENT 'Ӧ������',
  `user_erps` varchar(1000) DEFAULT NULL COMMENT '�û��б�',
  `apply_date` datetime NOT NULL COMMENT '����ʱ��',
  `approval_status` tinyint(4) NOT NULL COMMENT '����״̬0:���ͨ��1,�����2��˲�ͨ��',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID',
  `config_id` int(3) NOT NULL COMMENT '����ID',
  `version` varchar(32) DEFAULT NULL COMMENT '�汾',
  `settings` mediumtext COMMENT '�ͻ���������(JSON��ʾ)',
  `remark` varchar(255) DEFAULT NULL COMMENT '˵����ע',
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
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `update_date` datetime NOT NULL COMMENT '����ʱ��',
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����',
  `type` int(11) NOT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID',
  `tenant_id` varchar(60) NOT NULL COMMENT '�⻧id',
  `zone_id` bigint(20) NOT NULL COMMENT '������Ϣ',
  `current_capacity` bigint(20) NOT NULL COMMENT '��ǰ����',
  `capacity` bigint(20) NOT NULL COMMENT '��С',
  `status` int(11) NOT NULL COMMENT '״̬ 1:δ����,10:����redis,30:������,500:�����ͻ�������,1000:����ɹ�,-1000:����ʧ��',
  `update_time` datetime NOT NULL COMMENT '����ʱ��',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `update_by` varchar(30) DEFAULT NULL COMMENT '�޸���',
  `create_by` varchar(30) DEFAULT NULL COMMENT '������',
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
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����',
  `deploy_id` bigint(20) NOT NULL COMMENT '����ID',
  `deploy_type` int(11) NOT NULL,
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID',
  `tenant_id` varchar(60) NOT NULL,
  `shard_id` bigint(20) DEFAULT NULL COMMENT '��ƬID',
  `ip` varchar(32) DEFAULT NULL COMMENT 'ʵ��ip',
  `port` int(11) DEFAULT NULL COMMENT 'ʵ���˿�',
  `capacity` bigint(20) NOT NULL COMMENT '��С',
  `buckets_from` int(11) DEFAULT NULL,
  `buckets_to` int(11) DEFAULT NULL,
  `count` int(11) NOT NULL COMMENT 'ִ�д���',
  `status` int(11) NOT NULL COMMENT '״̬ 1:δ����,10������,1000:����ɹ�,-1000:����ʧ��',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `update_time` datetime NOT NULL COMMENT '�޸�ʱ��',
  `create_by` varchar(30) DEFAULT NULL COMMENT '������',
  `update_by` varchar(30) DEFAULT NULL COMMENT '�޸���',
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
  `name` varchar(50) NOT NULL COMMENT '����������',
  `type` varchar(20) NOT NULL COMMENT '����������',
  `ip` varchar(20) NOT NULL COMMENT '������IP',
  `jmx_port` int(11) NOT NULL DEFAULT '7654' COMMENT '������JMX�˿�',
  `description` varchar(500) DEFAULT NULL COMMENT '����',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `create_by` int(11) NOT NULL DEFAULT '0' COMMENT '������',
  `update_time` datetime NOT NULL COMMENT '�޸�ʱ��',
  `update_by` int(11) NOT NULL DEFAULT '0' COMMENT '�޸���',
  `status` int(4) NOT NULL DEFAULT '1' COMMENT '״̬(1���ã�0ͣ�ã�-1ɾ��)',
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
  `ip` varchar(64) NOT NULL COMMENT 'ip��ַ',
  `cpu` varchar(128) DEFAULT NULL COMMENT 'cpu��Ϣ',
  `disk` int(11) DEFAULT NULL COMMENT 'Ӳ��������λG',
  `memory` int(11) DEFAULT NULL COMMENT '�ڴ����� ��λG',
  `os` tinyint(3) DEFAULT NULL COMMENT '����ϵͳ0:windows,1:linux',
  `ethernet` tinyint(1) DEFAULT NULL COMMENT '���� 0:ǧ��,1:����',
  `zone` varchar(32) DEFAULT NULL COMMENT '����',
  `agent` tinyint(1) DEFAULT NULL COMMENT '�Ƿ���agent(Ĭ��0:��)',
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `modified_date` datetime NOT NULL COMMENT '����ʱ��',
  `created_user` varchar(30) NOT NULL COMMENT '������',
  `modified_user` varchar(30) NOT NULL COMMENT '�޸���',
  `switch_ip` varchar(30) DEFAULT NULL COMMENT '������ip',
  `remark` varchar(127) DEFAULT NULL COMMENT '��ע',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID/��ȺID',
  `shard_id` bigint(10) NOT NULL COMMENT '��ƬID',
  `copy_id` varchar(32) NOT NULL COMMENT '������ʶ',
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `modified_date` datetime NOT NULL COMMENT '�޸�ʱ��',
  `flag` tinyint(4) NOT NULL COMMENT '1: ��Ч�� 2: ��Ч',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID/��ȺID',
  `shard_id` bigint(10) DEFAULT NULL COMMENT '��ƬID',
  `copy_id` varchar(32) DEFAULT NULL COMMENT '������ʶ',
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `modified_date` datetime NOT NULL COMMENT '�޸�ʱ��',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID/��ȺID',
  `shard_id` bigint(10) NOT NULL COMMENT '��ƬID',
  `copy_id` varchar(32) NOT NULL COMMENT '������ʶ',
  `created_reason` varchar(255) DEFAULT '' COMMENT '����ԭ��',
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `created_by` varchar(128) NOT NULL DEFAULT '' COMMENT '����������¼��Ӧ������',
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
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
  `update_date` datetime NOT NULL COMMENT '����ʱ��',
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
  `created_date` datetime NOT NULL COMMENT '����ʱ��',
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
  `flag` tinyint(4) NOT NULL COMMENT '1: ��Ч��2����Ч',
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
  `uid` varchar(45) NOT NULL COMMENT 'ʵ��ID',
  `name` varchar(200) NOT NULL COMMENT '�ռ�����',
  `zone_id` bigint(20) NOT NULL COMMENT '����id',
  `capacity` bigint(20) NOT NULL COMMENT '������KB',
  `is_autoextend` tinyint(4) NOT NULL COMMENT '�Ƿ��Զ�����',
  `is_autofailover` tinyint(4) NOT NULL COMMENT '�Ƿ��Զ�failover',
  `password` varchar(64) DEFAULT NULL COMMENT '�ÿռ�ʵ����������',
  `cluster_type` tinyint(4) NOT NULL COMMENT '��Ⱥ���ͣ�1:������2:��Ⱥ',
  `created_date` datetime DEFAULT NULL COMMENT '����ʱ��',
  `modified_date` datetime DEFAULT NULL COMMENT '�޸�ʱ��',
  `created_user` varchar(30) DEFAULT NULL COMMENT '������(˭����ͨ������˭)',
  `modified_user` varchar(30) DEFAULT NULL COMMENT '�޸���',
  `is_lock` tinyint(4) DEFAULT NULL,
  `flag` tinyint(4) NOT NULL COMMENT '1: ��Ч�� 2�� ��Ч',
  `status` int(11) NOT NULL COMMENT '״̬ 0:������,100:ʹ����,200:������,500:����ʧ��,600:ɾ����,601:��ɾ�� ,602:ɾ��ʧ��',
  `tenant_id` varchar(100) NOT NULL COMMENT '�⻧id',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�id',
  `erp` varchar(50) NOT NULL COMMENT 'erp�˺�',
  `role` char(10) NOT NULL COMMENT '��ɫ(0��Ⱥ����Ա,1��Ⱥ�û�)',
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
  `name` varchar(50) NOT NULL COMMENT 'ϵͳ����',
  `level` tinyint(3) DEFAULT NULL COMMENT 'ϵͳ����',
  `levelDesc` varchar(20) DEFAULT NULL COMMENT 'ϵͳ��������',
  `leader` varchar(20) DEFAULT NULL COMMENT 'ϵͳ������',
  `oneLevelBranch` varchar(200) NOT NULL COMMENT 'һ������',
  `twoLevelBranch` varchar(200) NOT NULL COMMENT '��������',
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
  `type` varchar(50) NOT NULL COMMENT '��������',
  `refer_id` int(11) DEFAULT NULL COMMENT '����ID',
  `priority` tinyint(4) NOT NULL DEFAULT '0' COMMENT '���ȼ�',
  `daemons` tinyint(4) NOT NULL DEFAULT '0' COMMENT '�ػ�����',
  `owner` varchar(50) DEFAULT NULL COMMENT '������',
  `url` varchar(1000) DEFAULT NULL COMMENT '����',
  `cron` varchar(100) DEFAULT NULL COMMENT 'cron���ʽ',
  `dispatch_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '��������',
  `retry` tinyint(1) NOT NULL DEFAULT '0' COMMENT '�Ƿ�����',
  `retry_count` int(11) NOT NULL DEFAULT '0' COMMENT '���Դ���',
  `retry_time` datetime NOT NULL COMMENT '����ʱ��',
  `exception` varchar(2000) DEFAULT NULL COMMENT '�쳣',
  `create_by` varchar(30) DEFAULT NULL COMMENT '�����û�',
  `create_time` datetime NOT NULL COMMENT '����ʱ��',
  `update_by` varchar(30) DEFAULT NULL COMMENT '�����û�',
  `update_time` datetime NOT NULL COMMENT '����ʱ��',
  `status` tinyint(4) NOT NULL COMMENT '����״̬ 0:����;1:�ɷ�;2:ִ����;3:ִ�гɹ�;4:ʧ�ܣ�����Ҫ����;5:���;6:ʧ��,��Ҫ����;',
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
  `space_id` bigint(20) NOT NULL COMMENT '�ռ�ID',
  `epoch` int(15) DEFAULT NULL COMMENT '���ü�Ԫ�����ø��´���',
  `current_topology` mediumtext COMMENT '��ǰԪ��������',
  `temp_topology` mediumtext COMMENT '��ʱԪ����',
  `token` varchar(64) DEFAULT NULL COMMENT '�ͻ�������ƾ֤',
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
  `erp` varchar(50) NOT NULL COMMENT 'erp�˺�',
  `department1` varchar(50) DEFAULT NULL COMMENT 'һ������',
  `department2` varchar(50) DEFAULT NULL COMMENT '��������',
  `tel` varchar(30) DEFAULT NULL COMMENT '�û��绰',
  `mail` varchar(50) DEFAULT NULL COMMENT '�û�����',
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
