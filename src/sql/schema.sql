-- MySQL dump 10.13  Distrib 5.1.56, for pc-linux-gnu (x86_64)
--
-- Host: localhost    Database: biltv2
-- ------------------------------------------------------
-- Server version	5.1.56-log

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
-- Table structure for table `abon_abonent`
--

DROP TABLE IF EXISTS `abon_abonent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_abonent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `activated` datetime DEFAULT '2011-03-01 00:00:00',
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `sorting` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `bill_id` int(11) NOT NULL,
  `code` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `extid` int(10) unsigned NOT NULL DEFAULT '0',
  `confirmed` tinyint(1) NOT NULL DEFAULT '0',
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  `deactivated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_id` (`person_id`,`address_id`),
  KEY `abon_abonent_21b911c5` (`person_id`),
  KEY `abon_abonent_b213c1e9` (`address_id`),
  KEY `abon_abonent_bda51c3c` (`group_id`),
  KEY `abon_abonent_8ce2918d` (`bill_id`),
  KEY `extid` (`extid`)
) ENGINE=MyISAM AUTO_INCREMENT=22067 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_address`
--

DROP TABLE IF EXISTS `abon_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `building_id` int(11) NOT NULL,
  `flat` int(10) unsigned NOT NULL,
  `code` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `sorting` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `override` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sorting` (`sorting`),
  UNIQUE KEY `override` (`override`),
  UNIQUE KEY `building_id` (`building_id`,`flat`),
  KEY `abon_address_57000c84` (`building_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15233 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_bill`
--

DROP TABLE IF EXISTS `abon_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_bill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `balance` double NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22078 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_building`
--

DROP TABLE IF EXISTS `abon_building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_building` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `code` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `sorting` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sorting` (`sorting`),
  UNIQUE KEY `street_id` (`street_id`,`house_id`),
  KEY `abon_building_539ecf1b` (`street_id`),
  KEY `abon_building_1519731` (`house_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1123 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_city`
--

DROP TABLE IF EXISTS `abon_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `label` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_contact`
--

DROP TABLE IF EXISTS `abon_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `ctype` int(11) NOT NULL,
  `value` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `abon_contact_21b911c5` (`person_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_group`
--

DROP TABLE IF EXISTS `abon_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_house`
--

DROP TABLE IF EXISTS `abon_house`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `num` (`num`)
) ENGINE=MyISAM AUTO_INCREMENT=1325 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_person`
--

DROP TABLE IF EXISTS `abon_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `lastname` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `middlename` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `passport` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `registration` date NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `sorting` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `passport` (`passport`)
) ENGINE=MyISAM AUTO_INCREMENT=18088 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `abon_street`
--

DROP TABLE IF EXISTS `abon_street`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `abon_street` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_id` int(11) NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `sorting` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `city_id` (`city_id`,`name`),
  KEY `abon_street_586a73b5` (`city_id`)
) ENGINE=MyISAM AUTO_INCREMENT=241 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_user` (
  `user_ptr_id` int(11) NOT NULL,
  `icq` decimal(9,0) DEFAULT NULL,
  PRIMARY KEY (`user_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=123 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(75) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_abonent_active`
--

DROP TABLE IF EXISTS `data_abonent_active`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_abonent_active` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aa_id` int(11) DEFAULT NULL,
  `dac_id` int(11) DEFAULT NULL,
  `active` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17456 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_abonent_connect`
--

DROP TABLE IF EXISTS `data_abonent_connect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_abonent_connect` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `connect_id` int(10) unsigned NOT NULL,
  `person_id` int(10) unsigned NOT NULL,
  `active` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `connect_id` (`connect_id`,`person_id`,`active`),
  KEY `person_id` (`person_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18275 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_connect`
--

DROP TABLE IF EXISTS `data_connect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_connect` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `street_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `flat` mediumint(8) unsigned NOT NULL,
  `order` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `dogovor` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `remark` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `street_id` (`street_id`,`house_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24023 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_house`
--

DROP TABLE IF EXISTS `data_house`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_house` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `num` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=1325 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_intervals`
--

DROP TABLE IF EXISTS `data_intervals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_intervals` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `iac` int(11) unsigned NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `cost` mediumint(8) unsigned NOT NULL,
  `months` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iac` (`iac`)
) ENGINE=MyISAM AUTO_INCREMENT=72514 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_person`
--

DROP TABLE IF EXISTS `data_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_person` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fio` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pasport` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `comment` text COLLATE utf8_unicode_ci NOT NULL,
  `idkat` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18079 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_proplata`
--

DROP TABLE IF EXISTS `data_proplata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_proplata` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `iac` int(11) unsigned NOT NULL,
  `d1` date NOT NULL,
  `d2` date NOT NULL,
  `sum` float unsigned NOT NULL,
  `year` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `month` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iac` (`iac`)
) ENGINE=MyISAM AUTO_INCREMENT=1186765 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_psum`
--

DROP TABLE IF EXISTS `data_psum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_psum` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) unsigned DEFAULT NULL,
  `sum` float(9,3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17215 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_status`
--

DROP TABLE IF EXISTS `data_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_status` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `iac` bigint(20) unsigned NOT NULL,
  `ic` bigint(20) unsigned NOT NULL,
  `begin` date DEFAULT NULL,
  `end` date DEFAULT NULL,
  `start` date DEFAULT NULL,
  `s1` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `s2` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `finish` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `iac` (`iac`,`ic`),
  KEY `begin` (`begin`)
) ENGINE=MyISAM AUTO_INCREMENT=37982 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_street`
--

DROP TABLE IF EXISTS `data_street`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_street` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=241 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_tar`
--

DROP TABLE IF EXISTS `data_tar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_tar` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idk` smallint(5) unsigned NOT NULL,
  `cost` float NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idk` (`idk`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=139 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logger_log`
--

DROP TABLE IF EXISTS `logger_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logger_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `oid` int(10) unsigned NOT NULL,
  `data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logger_log_fbfc09f1` (`user_id`),
  KEY `logger_log_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_card`
--

DROP TABLE IF EXISTS `tv_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `activated` datetime NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `num` (`num`),
  KEY `tv_card_5d52dd10` (`owner_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17483 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_cardhistory`
--

DROP TABLE IF EXISTS `tv_cardhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_cardhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `date` date DEFAULT NULL,
  `card_id` int(11) NOT NULL,
  `action` smallint(5) unsigned NOT NULL,
  `oid` int(10) unsigned NOT NULL,
  `descr` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `tv_cardhistory_bbe27cfa` (`card_id`)
) ENGINE=MyISAM AUTO_INCREMENT=65275 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_cardservice`
--

DROP TABLE IF EXISTS `tv_cardservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_cardservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `card_id` int(11) NOT NULL,
  `tp_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  `activated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tv_cardservice_bbe27cfa` (`card_id`),
  KEY `tv_cardservice_9b5d2b2` (`tp_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17481 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_channel`
--

DROP TABLE IF EXISTS `tv_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_fee`
--

DROP TABLE IF EXISTS `tv_fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_fee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `bill_id` int(11) NOT NULL,
  `card_id` int(11) DEFAULT NULL,
  `sum` double NOT NULL,
  `prev` double NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `maked` tinyint(1) NOT NULL,
  `rolled_by_id` int(11) DEFAULT NULL,
  `descr` longtext COLLATE utf8_unicode_ci NOT NULL,
  `inner_descr` longtext COLLATE utf8_unicode_ci NOT NULL,
  `tp_id` int(11) DEFAULT NULL,
  `fee_type_id` int(11) DEFAULT NULL,
  `admin_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rolled_by_id` (`rolled_by_id`),
  KEY `tv_fee_8ce2918d` (`bill_id`),
  KEY `tv_fee_bbe27cfa` (`card_id`),
  KEY `tv_fee_9b5d2b2` (`tp_id`),
  KEY `tv_fee_ad8b5571` (`fee_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1412846 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_feecustomranges`
--

DROP TABLE IF EXISTS `tv_feecustomranges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_feecustomranges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interval_id` int(11) NOT NULL,
  `fee_type_id` int(11) NOT NULL,
  `startday` smallint(5) unsigned NOT NULL,
  `endday` smallint(5) unsigned NOT NULL,
  `sum` double NOT NULL,
  `ret` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tv_feecustomranges_17d2d99d` (`interval_id`),
  KEY `tv_feecustomranges_ad8b5571` (`fee_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_feeintervals`
--

DROP TABLE IF EXISTS `tv_feeintervals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_feeintervals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` date NOT NULL,
  `end` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_feeranges`
--

DROP TABLE IF EXISTS `tv_feeranges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_feeranges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interval_id` int(11) NOT NULL,
  `fee_type_id` int(11) NOT NULL,
  `sum` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tv_feeranges_17d2d99d` (`interval_id`),
  KEY `tv_feeranges_ad8b5571` (`fee_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_feescalendar`
--

DROP TABLE IF EXISTS `tv_feescalendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_feescalendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_feetype`
--

DROP TABLE IF EXISTS `tv_feetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_feetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `ftype` smallint(5) unsigned NOT NULL,
  `allow_negative` tinyint(1) NOT NULL,
  `sum` double NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_payment`
--

DROP TABLE IF EXISTS `tv_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `bill_id` int(11) NOT NULL,
  `sum` double NOT NULL,
  `prev` double NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `maked` tinyint(1) NOT NULL,
  `rolled_by_id` int(11) DEFAULT NULL,
  `descr` longtext COLLATE utf8_unicode_ci NOT NULL,
  `inner_descr` longtext COLLATE utf8_unicode_ci NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `source_id` int(11) DEFAULT '1',
  `register_id` int(11) DEFAULT NULL,
  `bank_date` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rolled_by_id` (`rolled_by_id`),
  KEY `tv_payment_8ce2918d` (`bill_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1136717 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_paymentregister`
--

DROP TABLE IF EXISTS `tv_paymentregister`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_paymentregister` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `total` double NOT NULL,
  `closed` tinyint(1) NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `bank` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tv_paymentregister_89f89e85` (`source_id`)
) ENGINE=MyISAM AUTO_INCREMENT=166 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_paymentregisterstamp`
--

DROP TABLE IF EXISTS `tv_paymentregisterstamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_paymentregisterstamp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `register_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tv_paymentregisterstamp_f663063` (`register_id`),
  KEY `tv_paymentregisterstamp_e972820` (`admin_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_paymentsource`
--

DROP TABLE IF EXISTS `tv_paymentsource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_paymentsource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `descr` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_tariffplan`
--

DROP TABLE IF EXISTS `tv_tariffplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_tariffplan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_tariffplanchannelrelationship`
--

DROP TABLE IF EXISTS `tv_tariffplanchannelrelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_tariffplanchannelrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tp_id` int(11) NOT NULL,
  `chrel_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tp_id` (`tp_id`,`chrel_id`),
  KEY `tv_tariffplanchannelrelationship_9b5d2b2` (`tp_id`),
  KEY `tv_tariffplanchannelrelationship_a4e0f91d` (`chrel_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_tariffplanfeerelationship`
--

DROP TABLE IF EXISTS `tv_tariffplanfeerelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_tariffplanfeerelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tp_id` int(11) NOT NULL,
  `fee_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tp_id` (`tp_id`,`fee_type_id`),
  KEY `tv_tariffplanfeerelationship_9b5d2b2` (`tp_id`),
  KEY `tv_tariffplanfeerelationship_ad8b5571` (`fee_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_trunk`
--

DROP TABLE IF EXISTS `tv_trunk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_trunk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `cached` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `comment` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `num` (`num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tv_trunkchannelrelationship`
--

DROP TABLE IF EXISTS `tv_trunkchannelrelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_trunkchannelrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trunk_id` int(11) NOT NULL,
  `slot` int(11) DEFAULT NULL,
  `channel_id` int(11) NOT NULL,
  `encoded` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `trunk_id` (`trunk_id`,`channel_id`),
  KEY `tv_trunkchannelrelationship_a4528ba1` (`trunk_id`),
  KEY `tv_trunkchannelrelationship_f9972756` (`channel_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-09-05 17:30:52
