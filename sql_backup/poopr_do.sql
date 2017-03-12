-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 22, 2017 at 01:21 PM
-- Server version: 5.7.16-0ubuntu0.16.04.1
-- PHP Version: 7.0.8-0ubuntu0.16.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `poopr_do`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `confirms_confirm_by_id_user` (IN `f` INT, IN `u` VARCHAR(255) CHARSET utf8)  NO SQL
INSERT INTO poopr_confirms 
(f_id, user)
VALUES (f,u)$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `confirms_get_by_id_user` ()  NO SQL
SELECT time FROM poopr_confirms WHERE user = u AND f_id = f$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `disputes_clear_disputes_by_id` (IN `f` INT)  NO SQL
UPDATE poopr_disputes SET cleared = TRUE where f_id = f$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `disputes_dispute_by_id_user` (IN `f` INT, IN `u` VARCHAR(255) CHARSET utf8)  NO SQL
INSERT INTO poopr_disputes (f_id,user) VALUES (f,u)$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_confirm_by_id` (IN `f` INT)  UPDATE poopr_facilities SET confirmation = confirmation + 1 WHERE id = f$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_dispute_by_id` (IN `f_id` INT)  NO SQL
UPDATE `poopr_facilities` SET `contested` = TRUE WHERE `id` = f_id$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_get_by_coordinate` (IN `lower_lon` FLOAT, IN `upper_lon` FLOAT, IN `lower_lat` FLOAT, IN `upper_lat` FLOAT)  NO SQL
SELECT * FROM `poopr_facilities`
    WHERE (lon BETWEEN
        CASE WHEN lower_lon <= upper_lon THEN lower_lon ELSE upper_lon END
        AND
        CASE WHEN lower_lon <= upper_lon THEN upper_lon ELSE lower_lon END
        )
        AND
        (lat BETWEEN
        CASE WHEN lower_lat <= upper_lat THEN lower_lat ELSE upper_lat END
        AND
        CASE WHEN lower_lat <= upper_lat THEN upper_lat ELSE lower_lat END
        )$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_get_by_id` (IN `f_id` INT)  NO SQL
SELECT * FROM `poopr_facilities` WHERE `id` = f_id$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_remove_dispute_by_id` (IN `f_id` INT)  NO SQL
UPDATE `poopr_facilities` SET `contested` = FALSE WHERE `id` = f_id$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `facilities_verify_existence_by_id` (IN `f_id` INT)  NO SQL
SELECT 1 FROM poopr_facilities WHERE id = f_id$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `ratings_get_by_id_user` (IN `f` INT, IN `u` VARCHAR(255) CHARSET utf8)  NO SQL
SELECT time FROM poopr_ratings where user = u AND f_id = f$$

CREATE DEFINER=`pooprDBr`@`localhost` PROCEDURE `ratings_rate_by_id_rating_user` (IN `f` INT, IN `r` INT, IN `u` VARCHAR(255) CHARSET utf8)  NO SQL
INSERT INTO poopr_ratings (f_id,rating,user)
VALUES (f,r,u)$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `poopr_confirms`
--

CREATE TABLE `poopr_confirms` (
  `id` int(11) NOT NULL,
  `f_id` int(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `poopr_confirms`
--

INSERT INTO `poopr_confirms` (`id`, `f_id`, `user`, `time`) VALUES
(1, 2, 'asdf', '2017-01-15 19:16:47'),
(2, 4, 'zuuzu', '2017-01-15 19:30:17'),
(3, 6, 'asdsad', '2017-01-15 20:33:43'),
(4, 10, 'asdfgh', '2017-01-15 20:38:47'),
(5, 2, 'asdf', '2017-01-15 21:03:04'),
(6, 2, 'asdf', '2017-01-15 21:03:19'),
(7, 2, 'asdf', '2017-01-15 21:03:28'),
(8, 2, 'asdf', '2017-01-15 21:03:36'),
(9, 2, 'asdf', '2017-01-15 21:06:22'),
(10, 9, 'asdf', '2017-01-15 23:01:15');

-- --------------------------------------------------------

--
-- Table structure for table `poopr_disputes`
--

CREATE TABLE `poopr_disputes` (
  `id` int(11) NOT NULL,
  `f_id` int(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cleared` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `poopr_disputes`
--

INSERT INTO `poopr_disputes` (`id`, `f_id`, `user`, `time`, `cleared`) VALUES
(1, 5, 'asdf', '2017-01-15 23:19:22', 0);

-- --------------------------------------------------------

--
-- Table structure for table `poopr_facilities`
--

CREATE TABLE `poopr_facilities` (
  `id` int(11) NOT NULL,
  `title` varchar(128) COLLATE utf8_bin NOT NULL,
  `lat` float NOT NULL,
  `lon` float NOT NULL,
  `description` text COLLATE utf8_bin,
  `imagepath` varchar(256) COLLATE utf8_bin DEFAULT NULL,
  `free` tinyint(1) NOT NULL,
  `sex` set('male','female') COLLATE utf8_bin NOT NULL,
  `unisex` tinyint(1) NOT NULL,
  `services` set('urinal','toilet','handicapped','changing_room','changing_station','shower') COLLATE utf8_bin NOT NULL,
  `rating` int(1) NOT NULL COMMENT '1 to 5',
  `confirmation` int(6) NOT NULL,
  `contested` tinyint(1) NOT NULL,
  `creator` varchar(128) COLLATE utf8_bin NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `poopr_facilities`
--

INSERT INTO `poopr_facilities` (`id`, `title`, `lat`, `lon`, `description`, `imagepath`, `free`, `sex`, `unisex`, `services`, `rating`, `confirmation`, `contested`, `creator`, `created`) VALUES
(1, 'test facility', 11.1111, 22.2344, NULL, NULL, 0, '', 0, '', 0, 4, 1, '', '2016-11-24 19:22:33'),
(2, 'Test Facility Cork', 51.8994, -8.4762, NULL, NULL, 0, '', 0, '', 2, 9, 0, '', '2016-11-24 19:22:33'),
(3, '1', 1, 1, '1', '1', 1, 'male', 1, 'urinal', 1, 4, 1, '1', '2016-11-24 21:46:38'),
(4, '1', 1, 1, '1', '1', 1, 'male', 1, 'urinal', 1, 2, 1, '1', '2016-11-24 21:49:31'),
(5, 'test title', 1, 1, '1', '1', 1, 'male', 1, 'urinal', 1, 1, 1, '1', '2016-12-04 12:45:12'),
(8, 'test title 2', 1, 1, '1', '1', 1, 'male', 1, 'urinal', 1, 1, 1, '1', '2016-12-04 12:50:23'),
(9, 'test title 3', 1, 1, '1', '1', 1, 'male', 1, 'urinal', 1, 2, 1, '1', '2016-12-04 12:51:22'),
(10, 'Test coordinates 1', 50, 50, NULL, NULL, 1, 'male,female', 1, 'urinal,toilet,handicapped,changing_room', 1, 2, 1, '1', '2016-12-27 12:49:02'),
(11, 'Test Coordinates 2', -50, -50, NULL, NULL, 1, 'male', 1, 'urinal', 1, 1, 1, '1', '2016-12-27 12:49:02'),
(12, 'Test Coordinates 3', 50.5, 50.5, '1', NULL, 1, 'female', 1, 'toilet,handicapped', 1, 1, 1, '1', '2016-12-27 12:50:32'),
(13, 'Test Alpha', 50.0001, 49.9999, 'asdfasdokjf', NULL, 0, 'male,female', 0, 'urinal,toilet,changing_room,shower', 4, 1, 0, 'asdfsdf', '2017-01-07 15:17:42'),
(14, 'Test Beta', 49.9999, 50.0001, 'asdfasf', NULL, 0, 'male,female', 0, 'urinal,toilet', 3, 1, 0, '', '2017-01-07 15:21:17');

-- --------------------------------------------------------

--
-- Table structure for table `poopr_ratings`
--

CREATE TABLE `poopr_ratings` (
  `id` int(11) NOT NULL,
  `f_id` int(11) NOT NULL,
  `user` varchar(255) COLLATE utf8_bin NOT NULL,
  `rating` tinyint(4) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `poopr_ratings`
--

INSERT INTO `poopr_ratings` (`id`, `f_id`, `user`, `rating`, `time`) VALUES
(1, 1, 'testuser', 3, '2017-01-15 15:22:02'),
(2, 2, 'asdf', 4, '2017-01-15 15:24:11'),
(3, 2, '12', 3, '2017-01-15 22:30:40'),
(4, 4, '12', 3, '2017-01-15 23:12:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `poopr_confirms`
--
ALTER TABLE `poopr_confirms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `poopr_disputes`
--
ALTER TABLE `poopr_disputes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `poopr_facilities`
--
ALTER TABLE `poopr_facilities`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `poopr_ratings`
--
ALTER TABLE `poopr_ratings`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `poopr_confirms`
--
ALTER TABLE `poopr_confirms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `poopr_disputes`
--
ALTER TABLE `poopr_disputes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `poopr_facilities`
--
ALTER TABLE `poopr_facilities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `poopr_ratings`
--
ALTER TABLE `poopr_ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
