CREATE TABLE `crawler_xiabb.weibo_post` (
  `id` varchar(45) NOT NULL,
  `body` text,
  `pub_time` varchar(45) DEFAULT NULL,
  `userid` varchar(45) DEFAULT NULL,
  `num_repost` int(11) DEFAULT '0',
  `source` varchar(45) DEFAULT NULL,
  `num_like` int(11) DEFAULT '0',
  `num_comment` int(11) DEFAULT '0',
  `location` varchar(45) DEFAULT NULL,
  `dt_insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `weibo_profile` (
  `userid` varchar(45) NOT NULL,
  `nick_name` varchar(45) DEFAULT NULL,
  `num_fan` int(11) DEFAULT '0',
  `num_follow` int(11) DEFAULT '0',
  `num_post` int(11) DEFAULT '0',
  `province` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `signature` text DEFAULT NULL,
  `url` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `dt_insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `birthday` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
