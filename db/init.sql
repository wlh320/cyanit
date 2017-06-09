############################### CYANIT DATABASE #######################################
DROP DATABASE IF EXISTS `cyanit`;
CREATE DATABASE `cyanit`;
USE `cyanit`;
#######################################################################################

############################### TABLE #######################################

-- 角色表 存放系统中所有的角色信息
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(63) NOT NULL DEFAULT '',
    `desc` varchar(255) NOT NULL DEFAULT ''
);


-- 用户表 存放用户的基本信息
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255)  NOT NULL DEFAULT '',
    `email` varchar(255)  NOT NULL DEFAULT '',
    `password` varchar(255) NOT NULL DEFAULT '',
    `rid` int(10) unsigned NOT NULL,
    
    FOREIGN KEY (`rid`) REFERENCES `role`(`id`)
);

-- 节点表 存放子节点信息
DROP TABLE IF EXISTS `node`;
CREATE TABLE `node` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255) NOT NULL DEFAULT '',
    `desc` varchar(1023) NOT NULL DEFAULT '',
    `deleted` boolean NOT NULL
);

-- 帖子表 存放帖子的信息
DROP TABLE IF EXISTS `thread`;
CREATE TABLE `thread` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` varchar(1023) NOT NULL,
    `uid` int(10) unsigned NOT NULL,
    `nid` int(10) unsigned NOT NULL,
    `creat_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `content` varchar(8191) NOT NULL,
    `vote` int(11) NOT NULL DEFAULT '0',
    `deleted` boolean NOT NULL,

    FOREIGN KEY (`uid`) REFERENCES `user`(`id`),
    FOREIGN KEY (`nid`) REFERENCES `node`(`id`)
);

-- 评论表 存放每个帖子的评论
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `uid` int(10) unsigned NOT NULL,
    `tid` int(10) unsigned NOT NULL,
    `creat_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `content` varchar(8191)  NOT NULL,
    `floor` int(10) unsigned NOT NULL,
    `vote` int(11) NOT NULL DEFAULT '0',
    `deleted` boolean NOT NULL,

    FOREIGN KEY (`uid`) REFERENCES `user`(`id`),
    FOREIGN KEY (`tid`) REFERENCES `thread`(`id`)
);

-- 帖子投票表 存放当前的投票信息
DROP TABLE IF EXISTS `vote_thread`;
CREATE TABLE `vote_thread`(
    `uid` int(10) unsigned NOT NULL,
    `tid` int(10) unsigned NOT NULL,
    `is_up` boolean NOT NULL,

    PRIMARY KEY (`uid`, `tid`),
    FOREIGN KEY (`uid`) REFERENCES `user`(`id`),
    FOREIGN KEY (`tid`) REFERENCES `thread`(`id`)
);

-- 评论投票表 存放当前的投票信息
DROP TABLE IF EXISTS `vote_comment`;
CREATE TABLE `vote_comment`(
    `uid` int(10) unsigned NOT NULL,
    `cid` int(10) unsigned NOT NULL,
    `is_up` boolean NOT NULL,

    PRIMARY KEY (`uid`, `cid`),
    FOREIGN KEY (`uid`) REFERENCES `user`(`id`),
    FOREIGN KEY (`cid`) REFERENCES `comment`(`id`)
);

#############################################################################

############################### CONST DATA ############################################
LOCK TABLES `role` WRITE;
INSERT INTO `role` VALUES (1, 'admin', '系统管理员'),(2, 'user', '普通用户'),(3, 'mute', '被禁言用户');
UNLOCK TABLES; 


#################################################################################

############################### PROCEDURE #######################################

-- ####################### 1.登录注册 ############################
-- -- 检查登录过程
-- DROP PROCEDURE IF EXISTS `validate_login`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `validate_login`(
-- IN p_username VARCHAR(255)
-- )
-- BEGIN
--     select * from user where name = p_username;
-- END //
-- DELIMITER ;

-- -- 注册 插入用户过程
-- DROP PROCEDURE IF EXISTS `create_user`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
--     IN p_name VARCHAR(255),
--     IN p_email VARCHAR(255),
--     IN p_password VARCHAR(255)
-- )
-- BEGIN
--     if ( select exists (select 1 from user where name = p_name) ) THEN
--         select '用户名已存在 !!';
     
--     ELSE
--         insert into user
--         (id, name, email, password)
--         values
--         (NULL, p_name, p_email, p_password);

--     END IF;
-- END //
-- DELIMITER ;
-- ####################################################################

-- ####################### 2.发帖,显示帖子 ############################
-- -- 获取所有的帖子
-- DROP PROCEDURE IF EXISTS `get_allpost`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `get_allpost`(

-- )
-- BEGIN
--     SELECT a.id,a.title,b.name,a.creat_time,a.vote,c.name
--     FROM `post` a JOIN `user` b JOIN `node` c
--     ON a.userid = b.id and a.nodeid = c.id
--     ORDER BY vote DESC, creat_time DESC;
-- END //
-- DELIMITER ;

-- -- 获取某个节点的帖子
-- DROP PROCEDURE IF EXISTS `get_post_from_node`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `get_post_from_node`(
--     IN p_nodeid int(10)
-- )
-- BEGIN
--     SELECT a.id,a.title,b.name,a.creat_time,a.vote,c.name
--     FROM `post` a JOIN `user` b JOIN `node` c
--     ON a.userid = b.id and a.nodeid = c.id
--     WHERE a.nodeid = p_nodeid
--     ORDER BY vote DESC, creat_time DESC;
-- END //
-- DELIMITER ;

-- -- 获取某个帖子
-- DROP PROCEDURE IF EXISTS `get_a_post`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `get_a_post`(
--     IN p_postid int(10)
-- )
-- BEGIN
--     SELECT a.id,a.title,b.name,a.creat_time,a.vote,a.content
--     FROM `post` a JOIN `user` b
--     ON a.userid = b.id and a.id = p_postid;
-- END //
-- DELIMITER ;

-- -- 发帖
-- DROP PROCEDURE IF EXISTS `post_poster`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `post_poster`(
--     IN p_userid int(10),
--     IN p_nodeid int(10),
--     IN p_title varchar(1023),
--     IN p_content varchar(8191)
-- )
-- BEGIN
--     INSERT INTO `post`
--     (id, title, userid, nodeid, creat_time, content, vote)
--     VALUES 
--     (NULL, p_title, p_userid, p_nodeid, now(), p_content, 0);
-- END //
-- DELIMITER ;
-- ###################################################################

-- ############################ 3.回复 显示回复 ######################
-- -- 获取某帖子所有的回复
-- DROP PROCEDURE IF EXISTS `get_comment`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `get_comment`(
--     IN p_postid int(10)
-- )
-- BEGIN
--     SELECT a.id,b.name,a.creat_time,a.content, a.floor, a.vote
--     FROM `comment` a JOIN `user` b 
--     ON a.userid = b.id and a.postid = p_postid
--     ORDER BY vote DESC, floor;
-- END //
-- DELIMITER ;

-- -- 回复某个帖子
-- DROP PROCEDURE IF EXISTS `post_comment`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `post_comment`(
--     IN p_userid int(10),
--     IN p_postid int(10),
--     IN p_content varchar(8191)
-- )
-- BEGIN
--     INSERT INTO `comment`
--     (id, userid, postid, creat_time, content, floor, vote)
--     SELECT NULL, p_userid, p_postid, now(), p_content, count(*)+2, 0
--     FROM `comment`
--     WHERE postid = p_postid;
-- END //
-- DELIMITER ;
-- #############################################################

-- ############################ 4.顶,踩 ########################
-- -- 顶,踩帖子
-- DROP PROCEDURE IF EXISTS `vote_poster`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `vote_poster`(
--     IN p_postid int(10),
--     IN p_value smallint(1)
-- )
-- BEGIN
--     UPDATE `post` SET
--     vote = vote + p_value
--     WHERE id = p_postid;
-- END //
-- DELIMITER ;

-- -- 顶,踩评论
-- DROP PROCEDURE IF EXISTS `vote_comment`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `vote_comment`(
--     IN p_commentid int(10),
--     IN p_votevalue smallint(1)
-- )
-- BEGIN
--     UPDATE `comment` SET
--     vote = vote + p_votevalue
--     WHERE id = p_postid;
-- END //
-- DELIMITER ;
-- #############################################################

-- ##################### 5. 节点相关 ###########################
-- DROP PROCEDURE IF EXISTS `get_all_node`;
-- DELIMITER //
-- CREATE DEFINER=`root`@`localhost` PROCEDURE `get_all_node`(
-- )
-- BEGIN
-- 	SELECT * FROM node;
-- END //
-- DELIMITER ;
-- ############################################################# 


-- 查询点赞记录
-- select thread.*, vote_thread.is_up from `thread` left join `vote_thread` on thread.uid = 2 and thread.id = vote_thread.tid;
