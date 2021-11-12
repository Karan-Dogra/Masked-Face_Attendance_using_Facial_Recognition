-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 01, 2021 at 05:14 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendance-main`
--

-- --------------------------------------------------------

--
-- Table structure for table `child`
--

CREATE TABLE `child` (
  `info_id` int(11) DEFAULT NULL,
  `attendance` varchar(100) NOT NULL,
  `date1` date DEFAULT NULL,
  `entry_time` time DEFAULT NULL,
  `mask_status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `child`
--

INSERT INTO `child` (`info_id`, `attendance`, `date1`, `entry_time`, `mask_status`) VALUES
(1605, 'PRESENT', '2021-03-30', '10:33:00', 'MASK'),
(1605, 'PRESENT', '2021-04-01', '20:46:00', 'NO MASK'),
(1633, 'PRESENT', '2021-04-02', '11:42:00', 'MASK'),
(1605, 'PRESENT', '2021-04-02', '19:43:00', 'NO MASK'),
(1627, 'PRESENT', '2021-04-02', '19:44:00', 'NO MASK'),
(1605, 'PRESENT', '2021-04-04', '17:59:00', 'MASK'),
(2015, 'PRESENT', '2021-04-14', '14:56:00', 'MASK'),
(1627, 'PRESENT', '2021-04-13', '10:16:00', 'MASK'),
(2015, 'PRESENT', '2021-01-04', '14:56:00', 'MASK'),
(1627, 'PRESENT', '2021-02-24', '10:16:00', 'MASK'),
(1683, 'PRESENT', '2021-03-10', '11:20:00', 'MASK'),
(1683, 'PRESENT', '2021-02-16', '11:45:00', 'NO MASK'),
(1683, 'PRESENT', '2021-01-10', '13:56:00', 'MASK'),
(1683, 'PRESENT', '2021-02-21', '17:12:00', 'NO MASK'),
(2015, 'PRESENT', '2021-04-06', '14:24:00', 'NO MASK'),
(1627, 'PRESENT', '2021-03-23', '14:29:00', 'NO MASK'),
(1605, 'PRESENT', '2021-04-14', '21:32:00', 'NO MASK'),
(1605, 'PRESENT', '2021-04-15', '20:48:00', 'NO MASK'),
(1605, 'PRESENT', '2021-05-01', '20:39:00', 'NO MASK');

-- --------------------------------------------------------

--
-- Table structure for table `exit1`
--

CREATE TABLE `exit1` (
  `info_id` int(11) DEFAULT NULL,
  `date1` date DEFAULT NULL,
  `exit_time` time DEFAULT NULL,
  `mask_status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `exit1`
--

INSERT INTO `exit1` (`info_id`, `date1`, `exit_time`, `mask_status`) VALUES
(1605, '2021-04-14', '12:54:58', 'MASK'),
(2015, '2021-01-04', '22:47:00', 'MASK'),
(1683, '2021-01-10', '19:47:10', 'MASK'),
(1683, '2021-02-16', '22:34:00', 'NO MASK'),
(1683, '2021-02-21', '17:42:10', 'MASK'),
(1627, '2021-02-24', '18:57:00', 'MASK'),
(1683, '2021-03-10', '17:48:00', 'MASK'),
(1627, '2021-03-23', '23:28:00', 'NO MASK'),
(1605, '2021-04-30', '19:00:00', 'MASK'),
(1605, '2021-04-15', '20:48:00', 'NO MASK'),
(1605, '2021-05-01', '20:40:00', 'NO MASK');

-- --------------------------------------------------------

--
-- Table structure for table `info`
--

CREATE TABLE `info` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `info`
--

INSERT INTO `info` (`id`, `username`, `email`, `department`) VALUES
(1243, 'Sumit Helio', 'sumit@gmail.com', 'WEll'),
(1605, 'Karan Dogra', 'karan@gmail.com', 'CSE'),
(1627, 'Aparnam Saini', 'aparnam@gmail.com', 'Sports'),
(1633, 'Issha Sethi', 'issha@gmail.com', 'IT'),
(1683, 'Kriti Singh', 'kriti.cse@gmail.com', 'CSE'),
(2015, 'Rohini Sharma', 'rohini@gmail.com', 'Civil');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `PASSWORD` varchar(100) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `Access` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`id`, `email`, `PASSWORD`, `username`, `Access`) VALUES
(1243, 'sumit@gmail.com', 'helloworld', 'Sumit Helio', 'Student'),
(1605, 'karan@gmail.com', 'helloworld', 'Karan Dogra', 'Admin'),
(1627, 'aparnam@gmail.com', 'password', 'Aparnam Saini', 'Student'),
(2015, 'rohini@gmail.com', 'rohini', 'Rohini Sharma', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `child`
--
ALTER TABLE `child`
  ADD UNIQUE KEY `info_id` (`info_id`,`date1`),
  ADD KEY `inf_ind` (`info_id`);

--
-- Indexes for table `exit1`
--
ALTER TABLE `exit1`
  ADD UNIQUE KEY `info_id` (`info_id`,`date1`),
  ADD KEY `infx_ind` (`info_id`);

--
-- Indexes for table `info`
--
ALTER TABLE `info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`,`username`,`email`,`department`),
  ADD KEY `in_id` (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `info`
--
ALTER TABLE `info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2018;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2016;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `child`
--
ALTER TABLE `child`
  ADD CONSTRAINT `child_ibfk_1` FOREIGN KEY (`info_id`) REFERENCES `info` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `exit1`
--
ALTER TABLE `exit1`
  ADD CONSTRAINT `exit1_ibfk_1` FOREIGN KEY (`info_id`) REFERENCES `info` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`id`) REFERENCES `info` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
