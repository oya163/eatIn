CREATE DATABASE  IF NOT EXISTS `eatin` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `eatin`;
-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: eatin
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Table structure for table `chef`
--

DROP TABLE IF EXISTS `chef`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chef` (
  `chefid` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(100) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zipcode` int(11) DEFAULT NULL,
  `countryid` int(11) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `userid` int(11) NOT NULL,
  `chefdbid` int(11) DEFAULT NULL,
  PRIMARY KEY (`chefid`),
  KEY `fk_chef_userid_idx` (`userid`),
  KEY `fk_chef_coutnryid_idx` (`countryid`),
  CONSTRAINT `fk_chef_coutnryid` FOREIGN KEY (`countryid`) REFERENCES `country` (`countryid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_chef_userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=98054 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chef_cnt`
--

DROP TABLE IF EXISTS `chef_cnt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chef_cnt` (
  `chefid` int(11) NOT NULL,
  `counter` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`chefid`),
  CONSTRAINT `fk_chef_cnt_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chefreachout`
--

DROP TABLE IF EXISTS `chefreachout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chefreachout` (
  `chefid` int(11) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `miles` int(11) DEFAULT NULL,
  KEY `fk_chefreachout_chefid_idx` (`chefid`),
  CONSTRAINT `fk_chefreachout_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chefspecial`
--

DROP TABLE IF EXISTS `chefspecial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chefspecial` (
  `chefid` int(11) NOT NULL,
  `cuisineid` int(11) NOT NULL,
  PRIMARY KEY (`chefid`,`cuisineid`),
  KEY `fk_chefspecial_cuisineid_idx` (`cuisineid`),
  KEY `fk_chefspecial_chefid_idx` (`chefid`),
  CONSTRAINT `fk_chefspecial_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_chefspecial_cuisineid` FOREIGN KEY (`cuisineid`) REFERENCES `cuisine` (`cuisineid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `countryid` int(11) NOT NULL AUTO_INCREMENT,
  `countryname` varchar(100) NOT NULL,
  `abbr` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`countryid`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuisine`
--

DROP TABLE IF EXISTS `cuisine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuisine` (
  `cuisineid` int(11) NOT NULL AUTO_INCREMENT,
  `cuisine_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cuisineid`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuisineitem`
--

DROP TABLE IF EXISTS `cuisineitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuisineitem` (
  `foodid` int(11) NOT NULL,
  `cuisineid` int(11) NOT NULL,
  PRIMARY KEY (`foodid`,`cuisineid`),
  KEY `fk_cuisineitem_foodid_idx` (`foodid`),
  KEY `fk_cuisineitem_cuisineid_idx` (`cuisineid`),
  CONSTRAINT `fk_cuisineitem_cuisineid` FOREIGN KEY (`cuisineid`) REFERENCES `cuisine` (`cuisineid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cuisineitem_foodid` FOREIGN KEY (`foodid`) REFERENCES `fooditem` (`foodid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `customerid` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(100) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zipcode` int(11) DEFAULT NULL,
  `countryid` int(11) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `preference` varchar(500) DEFAULT NULL,
  `userid` int(11) NOT NULL,
  PRIMARY KEY (`customerid`),
  KEY `fk_customer_userid_idx` (`userid`),
  KEY `fk_customer_countryid_idx` (`countryid`),
  CONSTRAINT `fk_customer_countryid` FOREIGN KEY (`countryid`) REFERENCES `country` (`countryid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_customer_userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2004 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fooditem`
--

DROP TABLE IF EXISTS `fooditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fooditem` (
  `foodid` int(11) NOT NULL AUTO_INCREMENT,
  `foodname` varchar(200) DEFAULT NULL,
  `food_des` varchar(500) DEFAULT NULL,
  `cook_time` int(11) DEFAULT NULL,
  `food_rating` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  `fn_id` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`foodid`)
) ENGINE=InnoDB AUTO_INCREMENT=68517 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fooditem_cnt`
--

DROP TABLE IF EXISTS `fooditem_cnt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fooditem_cnt` (
  `foodid` int(11) NOT NULL,
  `counter` int(11) DEFAULT NULL,
  PRIMARY KEY (`foodid`),
  CONSTRAINT `fk_fooditem_cnt_foodid` FOREIGN KEY (`foodid`) REFERENCES `fooditem` (`foodid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderfood`
--

DROP TABLE IF EXISTS `orderfood`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderfood` (
  `orderid` int(11) NOT NULL AUTO_INCREMENT,
  `customerid` int(11) NOT NULL,
  `chefid` int(11) NOT NULL,
  `foodid` int(11) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `req_date` datetime DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`orderid`),
  KEY `fk_orderfood_customerid_idx` (`customerid`),
  KEY `fk_orderfood_chefid_idx` (`chefid`),
  KEY `fk_orderfood_foodid_idx` (`foodid`),
  CONSTRAINT `fk_orderfood_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_orderfood_customerid` FOREIGN KEY (`customerid`) REFERENCES `customer` (`customerid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_orderfood_foodid` FOREIGN KEY (`foodid`) REFERENCES `fooditem` (`foodid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `eatin`.`orderfood_AFTER_INSERT` AFTER INSERT ON `orderfood` FOR EACH ROW
BEGIN
  IF EXISTS(SELECT * FROM fooditem_cnt WHERE fooditem_cnt.foodid = NEW.foodid) THEN
    UPDATE fooditem_cnt SET counter = (counter + 1)
    WHERE foodid = NEW.foodid;
  ELSE
    INSERT INTO fooditem_cnt (foodid, counter)
	VALUES(NEW.foodid, 1);
  END IF;
  
  IF EXISTS(SELECT * FROM chef_cnt WHERE chef_cnt.chefid = NEW.chefid) THEN
    UPDATE chef_cnt SET counter = (counter + 1)
    WHERE chefid = NEW.chefid;
  ELSE
    INSERT INTO chef_cnt (chefid, counter)
	VALUES(NEW.chefid, 1);
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=98119 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'eatin'
--
/*!50003 DROP PROCEDURE IF EXISTS `delete_chef` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_chef`(IN inchefid INT(11))
BEGIN
  START TRANSACTION;
  DELETE FROM chefreachout
  WHERE chefreachout.chefid = inchefid;
  DELETE FROM orderfood
  WHERE orderfood.chefid = inchefid;
  DELETE FROM chefspecial
  WHERE chefspecial.chefid = inchefid;
  DELETE FROM chef
  WHERE chef.chefid = inchefid;
  COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_customer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_customer`(IN incustid INT(11))
BEGIN
  START TRANSACTION;
  DELETE FROM orderfood
  WHERE orderfood.customerid = incustid;
  DELETE FROM customer
  WHERE customer.customerid = incustid;
  COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_all_chefs_details` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_chefs_details`()
BEGIN
  SELECT chef.userid, chef.chefid, user.fname, user.lname, country.countryid, country.countryname, cuisine.cuisineid, cuisine.cuisine_name
  FROM (((chef JOIN country ON chef.countryid = country.countryid)
    JOIN chefspecial ON chefspecial.chefid = chef.chefid)
    JOIN cuisine ON chefspecial.cuisineid = cuisine.cuisineid)
    JOIN user ON user.userid = chef.userid;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_chefs_by_food_id` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_chefs_by_food_id`(IN infoodid INT(11))
BEGIN
  SELECT chef.userid, chef.chefid, user.fname, user.lname, country.countryid, country.countryname
  FROM (((chefspecial JOIN chef ON chefspecial.chefid = chef.chefid)
    JOIN cuisineitem ON cuisineitem.cuisineid = chefspecial.cuisineid)
    JOIN user ON user.userid = chef.userid)
    JOIN country ON chef.countryid = country.countryid 
  WHERE cuisineitem.foodid = infoodid;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-21 22:53:33
