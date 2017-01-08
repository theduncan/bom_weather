-- phpMyAdmin SQL Dump
-- version 4.6.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 07, 2017 at 05:40 PM
-- Server version: 10.1.19-MariaDB-1~jessie
-- PHP Version: 5.6.27-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `weather`
--

-- --------------------------------------------------------

--
-- Table structure for table `Forecast_Description`
--

CREATE TABLE `Forecast_Description` (
  `ID` int(11) NOT NULL,
  `Product_ID` varchar(8) NOT NULL DEFAULT '********',
  `aac` varchar(10) NOT NULL,
  `parent-aac` varchar(10) NOT NULL,
  `Local_Start` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Local_End` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `UTC_Start` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `UTC_End` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Forecast_Description` text NOT NULL,
  `Fire_Danger` varchar(20) DEFAULT NULL,
  `UV_Alert` varchar(255) NOT NULL,
  `DateTime_Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `DateTime_Modified` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Radar`
--

CREATE TABLE `Radar` (
  `ID` int(11) NOT NULL,
  `Product_ID` varchar(8) NOT NULL DEFAULT '********',
  `STAMP` varchar(12) NOT NULL,
  `status` varchar(1) NOT NULL DEFAULT '0',
  `ext` varchar(4) NOT NULL,
  `url` varchar(255) NOT NULL,
  `timestamp_downloaded` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `timestamp_modified` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `timestamp_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Forecast_Description`
--
ALTER TABLE `Forecast_Description`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `aac` (`aac`,`Local_Start`,`Local_End`);

--
-- Indexes for table `Radar`
--
ALTER TABLE `Radar`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Product_ID` (`Product_ID`,`STAMP`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Forecast_Description`
--
ALTER TABLE `Forecast_Description`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Radar`
--
ALTER TABLE `Radar`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;