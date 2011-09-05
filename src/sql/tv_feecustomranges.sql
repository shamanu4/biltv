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
-- Dumping data for table `tv_feecustomranges`
--

LOCK TABLES `tv_feecustomranges` WRITE;
/*!40000 ALTER TABLE `tv_feecustomranges` DISABLE KEYS */;
INSERT INTO `tv_feecustomranges` VALUES (1,5,1,1,4,7,6),(2,5,1,5,8,6,5),(3,5,1,9,12,5,4),(4,5,1,13,16,4,3),(5,5,1,17,20,3,2),(6,5,1,21,24,2,1),(7,5,1,25,31,1,0),(11,4,1,4,6,9,8),(10,4,1,1,3,10,9),(12,4,1,7,9,8,7),(13,4,1,10,12,7,6),(14,4,1,13,15,6,5),(15,4,1,16,18,5,4),(16,4,1,19,21,4,3),(17,4,1,22,24,3,2),(18,4,1,25,27,2,1),(19,4,1,28,31,1,0),(20,3,1,1,2,15,14),(21,3,1,3,4,14,13),(22,3,1,5,6,13,12),(23,3,1,7,8,12,11),(24,3,1,9,10,11,10),(25,3,1,11,12,10,9),(26,3,1,13,14,9,8),(27,3,1,15,16,8,7),(28,3,1,17,18,7,6),(29,3,1,19,20,6,5),(30,3,1,21,22,5,4),(31,3,1,23,24,4,3),(32,3,1,25,26,3,2),(33,3,1,27,28,2,1),(34,3,1,29,31,1,0),(35,2,1,1,3,20,18),(36,2,1,4,6,18,16),(37,2,1,7,9,16,14),(38,2,1,10,12,14,12),(39,2,1,13,15,12,10),(40,2,1,16,18,10,8),(41,2,1,19,21,8,6),(42,2,1,22,24,6,4),(43,2,1,25,27,4,2),(44,2,1,28,31,2,0),(45,1,1,1,3,25,22.5),(46,1,1,4,6,22.5,20),(47,1,1,7,9,20,17.5),(48,1,1,10,12,17.5,15),(49,1,1,13,15,15,12.5),(50,1,1,16,18,12.5,10),(51,1,1,19,21,10,7.5),(52,1,1,22,24,7.5,5),(53,1,1,25,27,5,2.5),(54,1,1,28,31,2.5,0),(57,7,1,8,15,3,2),(56,7,1,1,7,4,3),(58,7,1,16,23,2,1),(59,7,1,24,31,1,0);
/*!40000 ALTER TABLE `tv_feecustomranges` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-09-05 17:32:58
