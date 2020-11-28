-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.8-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for monitoring
CREATE DATABASE IF NOT EXISTS `monitoring` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `monitoring`;

-- Dumping structure for table monitoring.agentdata
CREATE TABLE IF NOT EXISTS `agentdata` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `timestamp` int(10) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `monitor` varchar(250) NOT NULL,
  `value` decimal(50,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table monitoring.agentevents
CREATE TABLE IF NOT EXISTS `agentevents` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `timestamp` int(10) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `monitor` varchar(250) NOT NULL,
  `message` varchar(250) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `severity` varchar(11) NOT NULL,
  `processed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table monitoring.agentsystem
CREATE TABLE IF NOT EXISTS `agentsystem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` int(10) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `ipaddress` varchar(100) DEFAULT NULL,
  `platform` varchar(100) DEFAULT NULL,
  `build` varchar(100) DEFAULT NULL,
  `architecture` varchar(25) DEFAULT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `processors` int(10) unsigned DEFAULT NULL,
  `memory` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table monitoring.auth_group

CREATE TABLE IF NOT EXISTS `notifyrule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notify_name` varchar(100) NOT NULL,
  `notify_email` varchar(100) NOT NULL,
  `agent_name` varchar(100) NOT NULL,
  `agent_monitor` varchar(250) NOT NULL,
  `agent_status` tinyint(1) NOT NULL,
  `agent_severity` varchar(11) NOT NULL,
  `notify_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table monitoring.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(50) NOT NULL DEFAULT '0',
  `password` varchar(100) NOT NULL DEFAULT '0',
  `role` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
