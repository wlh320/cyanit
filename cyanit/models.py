# -*- coding:utf-8 -*-
"""models.py database models"""
from cyanit import db
from datetime import datetime


class User(db.Model):
    """用户Model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    rid = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, password):
        self.name = username
        self.email = email
        self.password = password
        self.rid = Role.ROLE_USER

    def __repr__(self):
        return '<User %r>' % self.name
    
    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'email':self.email, 
                'role':self.role.name, 'role_info':self.role.desc}


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), unique=True)
    desc = db.Column(db.String(255))

    ROLE_ADMIN = 1
    ROLE_USER = 2
    ROLE_MUTE = 3

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    @staticmethod
    def init_role():
        admin = Role('admin', '管理员')
        user  = Role('user', '普通用户')
        muter = Role('mute', '被禁言者')
        roles = [admin, user, muter]
        db.session.add_all(roles)
        db.session.commit()


class Node(db.Model):
    """节点Model"""
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    desc = db.Column(db.String(1023))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.deleted = False

    def __repr__(self):
        return '<Node %r>' % self.username

    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'desc':self.desc, 'deleted':self.deleted}


class Thread(db.Model):
    """帖子Model"""
    __tablename__ = 'thread'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1023))
    content = db.Column(db.String(1023))
    creat_time = db.Column(db.DateTime)
    vote = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, default=False)

    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('threads', lazy='dynamic'))
    nid = db.Column(db.Integer, db.ForeignKey('node.id'))
    node = db.relationship('Node', backref=db.backref('threads', lazy='dynamic'))

    def __init__(self, title, uid, nid, content):
        self.title = title
        self.uid = uid
        self.nid = nid
        self.content = content
        self.vote = 0
        self.creat_time = datetime.now()
        self.deleted = False

    def to_dict(self):
        return {'id':self.id, 'title':self.title, 'vote':self.vote, 'time':self.creat_time,
                'user':self.user.name, 'node':self.node.name, 'deleted':self.deleted}


class Comment(db.Model):
    """评论Model"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(8191))
    floor = db.Column(db.Integer)
    vote = db.Column(db.Integer)
    creat_time = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)

    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    tid = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship('Thread', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, content, uid, tid, floor):
        self.content = content
        self.uid = uid
        self.tid = tid
        self.vote = 0
        self.floor = floor
        self.creat_time = datetime.now()
        self.deleted = False
    
    def to_dict(self):
        return {'id':self.id, 'content':self.content, 'floor':self.floor, 'vote':self.vote,
                'user':self.user.name, 'time':self.creat_time, 'tid':self.tid, 'deleted':self.deleted}


class VoteThread(db.Model):
    """对帖子的点赞记录"""
    __tablename__ = 'vote_thread'
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('vote_thread', lazy='dynamic'))
    tid = db.Column(db.Integer, db.ForeignKey('thread.id'), primary_key=True)
    thread = db.relationship('Thread', backref=db.backref('vote_thread', lazy='dynamic'))
    is_up = db.Column(db.Boolean)

    def __init__(self, uid, tid, is_up):
        self.uid = uid
        self.tid = tid
        self.is_up = is_up


class VoteComment(db.Model):
    """对评论的点赞记录"""
    __tablename__ = 'vote_comment'
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('vote_comment', lazy='dynamic'))
    cid = db.Column(db.Integer, db.ForeignKey('comment.id'), primary_key=True)
    comment = db.relationship('Comment', backref=db.backref('vote_comment', lazy='dynamic'))
    is_up = db.Column(db.Boolean)

    def __init__(self, uid, cid, is_up):
        self.uid = uid
        self.cid = cid
        self.is_up = is_up
