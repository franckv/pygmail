SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `pygmail`
--

-- --------------------------------------------------------

--
-- Table `message`
--

CREATE TABLE IF NOT EXISTS `message` (
  `id` int(11) NOT NULL auto_increment,
  `from` varchar(50) default NULL,
  `subject` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;


-- --------------------------------------------------------

--
-- Table `message_tag`
--

CREATE TABLE IF NOT EXISTS `message_tag` (
  `message_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  KEY `.message_id` (`message_id`,`tag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table `path`
--

CREATE TABLE IF NOT EXISTS `path` (
  `message_id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  KEY `message_id` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table `tag`
--

CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

