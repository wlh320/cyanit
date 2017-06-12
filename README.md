# cyanit

a simple flask forum

also a coarse and not round reinvented wheel XD

Still under development...

一个造的不是很圆的论坛的轮子
功能和代码目前还不稳定

## Tech Stack

Database : MySQL + SQLAlchemy

Backend : python3 + Flask

Frontend : jQuery Bootstrap font-awesome Datatables ckeditor

## Functionalities

- register/login/logout 注册/登录
- post threads 发帖
- post comments 评论
- rich text 富文本(暂不支持上传)
- multi boards 多板块
- vote on threads/comments both dig & bury 顶/踩
- simple CMS dashboard:  简单的后台管理系统: 软删除各种东西还有禁言
  - soft delete / add boards
  - soft delete / restore threads
  - soft delete / restore comments
  - mute users


## Install & Run

0. Create Virtual Environment (**Optional**)

   ```
   pip install virtualenv
   virtualenv venv
   source venv/bin/activate
   ```

1. Install dependencies

   ```
   pip install -r requirements.txt
   ```

2. modify configs

   modify your db configs in `app/__init__.py`

   修改数据库等配置

3. Import database

   导入数据库

   ```
   mysql -u your-mysql-user -p < db/init.sql

   // You can import some data by:
   mysql -u your-mysql-user -p < db/data.sql
   ```

4. Run it!

   run

   ```
   python run.py
   ```

   and then you can visit `localhost:5000`


## TODO

- add more features to make it more powerful
  - private messages
  - unread threads/comments alert
  - ~~sort threads/comments not only by votes~~ sort threads/comments by both vote and time with their own weight
  - @  someone

- learn from existing projects to make my code more pythonic
