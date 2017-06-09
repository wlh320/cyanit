-- MySQL dump 10.16  Distrib 10.1.24-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: cyanit
-- ------------------------------------------------------
-- Server version	10.1.24-MariaDB

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
USE `cyanit`;


--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,1,1,'2017-06-06 15:42:39','<p>666</p>\r\n',1,0,0),(2,3,3,'2017-06-06 18:43:33','<p><strong>富文本用了</strong>&nbsp;ckeditor</p>\r\n\r\n<p><em>回帖测试</em></p>\r\n',1,0,0),(3,3,3,'2017-06-06 18:44:58','<p>testtest</p>\r\n',2,1,0),(4,4,3,'2017-06-06 18:46:07','<p>换个人回帖</p>\r\n',3,0,0),(5,4,4,'2017-06-06 18:47:46','<p>似乎能过滤简单的XSS</p>\r\n\r\n<p>超链接测试:<a href=\"http://www.google.com\">呵呵</a></p>\r\n',1,0,0),(6,4,6,'2017-06-06 18:51:36','<p>jquery</p>\r\n\r\n<p>MySQL 好用吗？</p>\r\n',1,0,0),(7,1,1,'2017-06-06 23:34:36','<p>hehehe</p>\r\n',2,0,0),(8,1,4,'2017-06-06 23:35:33','<p><strong>多加几条评论啊！让管理员页面能演示翻页</strong></p>\r\n',2,0,0),(9,1,4,'2017-06-06 23:35:42','<p>好的</p>\r\n',3,0,0),(10,1,5,'2017-06-06 23:36:05','<p>123123</p>\r\n',1,0,0),(11,1,5,'2017-06-06 23:36:09','<p>1232132</p>\r\n',2,0,0),(12,5,5,'2017-06-06 23:37:19','<p>asfdsd</p>\r\n',3,0,0),(13,5,5,'2017-06-06 23:37:31','<p>asfsdfdcdbfdrfd速度进入非个人缴费为偶发就分为非叫我</p>\r\n\r\n<p>围巾围殴</p>\r\n\r\n<p>问问我无法为范围而无法范围分为非为服务合同号</p>\r\n',4,0,0),(14,1,5,'2017-06-06 23:37:56','<p>再瞎发就禁言<strong>你俩</strong>！</p>\r\n',5,0,0),(15,1,7,'2017-06-06 23:42:47','<p>老夫敲代码就是一把梭.jpg</p>\r\n\r\n<p><img alt=\"\" src=\"https://pic2.zhimg.com/v2-e56dc170e9b026ca4ddb30c7cef7e3ed_b.jpg\" style=\"height:394px; width:600px\" /></p>\r\n',1,0,1),(16,1,7,'2017-06-06 23:45:14','<p>图片目前只支持url，暂不支持上传嘿嘿（服务器太渣</p>\r\n',2,0,0),(17,1,7,'2017-06-06 23:45:31','<p>1楼被吃辣</p>\r\n',3,0,0),(18,4,7,'2017-06-06 23:46:53','<p>老夫敲代码就是一把梭.jpg&nbsp;</p>\r\n\r\n<p><img alt=\"\" src=\"data:image/jpeg;base64,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',4,0,1),(19,1,7,'2017-06-06 23:51:16','<p><img alt=\"一把梭\" src=\"http://wx2.sinaimg.cn/mw690/005NVR7Rly1fgbx28adc0j30go0aztie.jpg\" style=\"height:198px; width:300px\" /></p>\r\n',5,0,0);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `node`
--

LOCK TABLES `node` WRITE;
/*!40000 ALTER TABLE `node` DISABLE KEYS */;
INSERT INTO `node` VALUES (1,'Testnode','Hello, world!',0),(2,'Database','You can discuss database in this node',0),(3,'Python','You can discuss python in this node',1),(4,'hehe','123',0),(5,'测试','测试测试测试测试测试测试 hello?',0);
/*!40000 ALTER TABLE `node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `thread`
--

LOCK TABLES `thread` WRITE;
/*!40000 ALTER TABLE `thread` DISABLE KEYS */;
INSERT INTO `thread` VALUES (1,'hehe',1,4,'2017-06-06 15:38:16','<p><strong>???</strong></p>\r\n',1,0),(2,'hello,world',1,2,'2017-06-06 15:57:51','<p><strong>TEST</strong></p>\r\n\r\n<p>呵呵呵呵呵</p>\r\n',0,0),(3,'新版本测试',3,1,'2017-06-06 18:42:39','<ol>\r\n	<li><strong>重写了大部分代码</strong></li>\r\n	<li><s>新版本测试</s></li>\r\n</ol>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<hr />\r\n<p>我是测试者。</p>\r\n',3,0),(4,'new thread',4,1,'2017-06-06 18:46:36','<p>&lt;script&gt;alert(&#39;1&#39;);&lt;/script&gt;</p>\r\n',1,0),(5,'123123123213123123',4,1,'2017-06-06 18:48:14','<p>123123123</p>\r\n',0,0),(6,'flask flask flask',4,3,'2017-06-06 18:50:25','<p><s>django!</s></p>\r\n\r\n<p><s>bottle!</s></p>\r\n\r\n<p><s>tornado!</s></p>\r\n\r\n<p><strong><em>flask!</em></strong></p>\r\n',0,1),(7,'图片测试',1,5,'2017-06-06 23:39:05','<p><img alt=\"滑稽图\" src=\"https://timgsa.baidu.com/timg?image&amp;quality=80&amp;size=b9999_10000&amp;sec=1497368351&amp;di=1a421d0bceca59e9719c770e95062e09&amp;imgtype=jpg&amp;er=1&amp;src=http%3A%2F%2Fe.hiphotos.baidu.com%2Fzhidao%2Fwh%253D450%252C600%2Fsign%3De831a02c33a85edffad9f6277c642515%2F359b033b5bb5c9ea41ceca9fd239b6003af3b389.jpg\" style=\"height:100px; width:100px\" />滑稽</p>\r\n',2,0),(8,'老夫写代码就用jQuery!',1,2,'2017-06-06 23:53:35','<p>不要给我说什么react/angular/vue!</p>\r\n\r\n<p>老夫写代码就用jQuery!</p>\r\n\r\n<p>复制！粘贴！</p>\r\n\r\n<p>拿起键盘就是干！</p>\r\n\r\n<p><img alt=\"\" src=\"http://wx3.sinaimg.cn/mw690/005NVR7Rly1fgbx2934fyj30go0b43yu.jpg\" style=\"height:333px; width:500px\" /></p>\r\n',1,0);
/*!40000 ALTER TABLE `thread` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'wlh','wlh233@163.com','pbkdf2:sha1:1000$E2I1giYC$6ab9f46264faf65aac70f901ed11a587321b6d94',1),(2,'wangshuheng','331349851@qq.com','pbkdf2:sha1:1000$cykfleDL$0f0fdac03da2f053643600905dd70e4a09204695',2),(3,'test','test@0hao.top','pbkdf2:sha1:1000$UMullFgL$a0235c16ccef26d234ecd3b33d834e7822652f0d',3),(4,'wlh320','wlh233@163.com','pbkdf2:sha1:1000$hteNzCsP$7fb5e89d00caaf2a3f1af39c19e15616097531bc',2),(5,'wlh123','wlh@123.com','pbkdf2:sha1:1000$z0Jf1kAM$c4eac3cae2c6c72517f8780623b4e9427dddd66c',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `vote_comment`
--

LOCK TABLES `vote_comment` WRITE;
/*!40000 ALTER TABLE `vote_comment` DISABLE KEYS */;
INSERT INTO `vote_comment` VALUES (3,3,1);
/*!40000 ALTER TABLE `vote_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vote_thread`
--

LOCK TABLES `vote_thread` WRITE;
/*!40000 ALTER TABLE `vote_thread` DISABLE KEYS */;
INSERT INTO `vote_thread` VALUES (1,1,1),(1,3,1),(1,7,1),(1,8,1),(3,3,1),(4,3,1),(4,4,1),(4,7,1);
/*!40000 ALTER TABLE `vote_thread` ENABLE KEYS */;
UNLOCK TABLES;

