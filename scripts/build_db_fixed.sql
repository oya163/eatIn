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
  `country` varchar(50) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `userid` int(11) NOT NULL,
  PRIMARY KEY (`chefid`),
  KEY `fk_chef_userid_idx` (`userid`),
  CONSTRAINT `fk_chef_userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
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
  KEY `fk_chefspecial_cuisineid_idx` (`cuisineid`),
  KEY `fk_chefspecial_chefid_idx` (`chefid`),
  CONSTRAINT `fk_chefspecial_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_chefspecial_cuisineid` FOREIGN KEY (`cuisineid`) REFERENCES `cuisine` (`cuisineid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `country` varchar(50) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `preference` varchar(500) DEFAULT NULL,
  `userid` int(11) NOT NULL,
  PRIMARY KEY (`customerid`),
  KEY `fk_customer_userid_idx` (`userid`),
  CONSTRAINT `fk_customer_userid` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fooditem`
--

DROP TABLE IF EXISTS `fooditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fooditem` (
  `foodid` int(11) NOT NULL AUTO_INCREMENT,
  `foodname` varchar(100) DEFAULT NULL,
  `food_des` varchar(500) DEFAULT NULL,
  `cook_time` varchar(10) DEFAULT NULL,
  `food_rating` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`foodid`)
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
  `cuisineid` int(11) NOT NULL,
  `order_date` datetime DEFAULT NULL,
  `req_date` datetime DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`orderid`),
  KEY `fk_orderfood_customerid_idx` (`customerid`),
  KEY `fk_orderfood_chefid_idx` (`chefid`),
  KEY `fk_orderfood_cuisineid_idx` (`cuisineid`),
  CONSTRAINT `fk_orderfood_chefid` FOREIGN KEY (`chefid`) REFERENCES `chef` (`chefid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_orderfood_cuisineid` FOREIGN KEY (`cuisineid`) REFERENCES `cuisine` (`cuisineid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_orderfood_customerid` FOREIGN KEY (`customerid`) REFERENCES `customer` (`customerid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-28 21:20:03
