SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS  `video_info_iqiyi_category`;
CREATE TABLE `video_info_iqiyi_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

insert into `video_info_iqiyi_category`(`category_id`,`category_name`) values
('1','欢乐精选'),
('2','娱乐八卦'),
('3','搞笑短片'),
('4','影视剧吐槽'),
('5','雷人囧事'),
('6','爆笑节目'),
('7','萌宠'),
('8','童趣'),
('9','奇闻趣事'),
('10','恶搞配音'),
('11','相声'),
('12','小品'),
('13','猎奇'),
('14','啪啪奇');
SET FOREIGN_KEY_CHECKS = 1;

