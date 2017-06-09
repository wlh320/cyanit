# -*- coding:utf-8 -*-
"""controllers.py some useful functions"""
from cyanit import db
from .models import Role, User, Thread, Comment, Node, VoteThread, VoteComment
from werkzeug.security import generate_password_hash, check_password_hash

############################ 功能函数 ################################
def get_all_nodes():
    """获取所有的节点"""
    nodes = Node.query.all()
    return [node.to_dict() for node in nodes]


def get_all_users():
    """获取所有用户"""
    users = User.query.all()
    return [user.to_dict() for user in users]


def get_all_threads():
    """获取所有帖子"""
    threads = Thread.query.order_by(Thread.vote.desc(), Thread.creat_time.desc()).all()
    return [thread.to_dict() for thread in threads]


def get_all_comments():
    """获取所有的评论"""
    comments = Comment.query.all()
    return [comment.to_dict() for comment in comments]


def get_all_threads_with_vote(uid):
    """获取所有帖子(带投票状态)"""
    qres = db.session.query(Thread, VoteThread.is_up).outerjoin(VoteThread, db.and_(VoteThread.uid==uid, VoteThread.tid == Thread.id)).order_by(Thread.vote.desc(), Thread.creat_time.desc()).all()
    threads = [thread[0].to_dict() for thread in qres]
    for (i,thread) in enumerate(threads):
        thread["vstatus"]=qres[i][1]
    return threads


def get_threads_by_nid(nid):
    """获取某个节点下的所有帖子"""
    node = Node.query.get(nid)
    threads = node.threads.order_by(Thread.vote.desc(), Thread.creat_time.desc())
    return [thread.to_dict() for thread in threads]


def get_threads_by_nid_with_vote(nid, uid):
    """获取某个节点下的所有帖子(带投票状态)"""
    qres = db.session.query(Thread, VoteThread.is_up).filter(Thread.nid == nid).outerjoin(VoteThread, db.and_(VoteThread.uid==uid, VoteThread.tid == Thread.id)).order_by(Thread.vote.desc(), Thread.creat_time.desc())
    threads = [thread[0].to_dict() for thread in qres]
    for (i,thread) in enumerate(threads):
        thread["vstatus"]=qres[i][1]
    return threads


def get_thread_by_tid(tid):
    """获取某个帖子的详细内容"""
    thread = Thread.query.get(tid)
    if not thread:
        return None
    res = thread.to_dict()
    res['content'] = thread.content;
    return res


def get_comments_by_tid(tid):
    """获取某个帖子的评论"""
    thread = Thread.query.get(tid)
    comments = thread.comments
    return [comment.to_dict() for comment in comments]


def get_comments_by_tid_with_vote(tid, uid):
    """获取某个帖子的评论"""
    qres = db.session.query(Comment, VoteComment.is_up).filter(Comment.tid == tid).outerjoin(VoteComment, db.and_(VoteComment.uid==uid, VoteComment.cid == Comment.id)).order_by(Comment.vote.desc(), Comment.floor)
    comments =  [comment[0].to_dict() for comment in qres]
    for (i, comment) in enumerate(comments):
        comment["vstatus"]=qres[i][1]
    return comments


def filter_deleted(datalist):
    """过滤掉被删除的东西"""
    filtered = filter(lambda d: d['deleted'] is False, datalist)
    return [item for item in filtered]


def do_register(username, email, password, p_confirm):
    """注册"""
    # 信息不全
    if not username and email and password and p_confirm:
        return {'error':'信息不全'}
    # 密码确认不匹配
    if password != p_confirm:
        return {'error':'密码两次输入不同'}
    # 已被注册
    if User.query.filter_by(name=username).first():
        return {'error':'用户名已被注册'}

    # 一切正常
    hash_p = generate_password_hash(password)
    new_user = User(username, email, hash_p)
    db.session.add(new_user)
    db.session.commit()
    return {'success':'success'}


def do_login(username, password):
    """登录"""
    user = User.query.filter_by(name=username).first()
    # 用户名不存在
    if not user:
        return {'error':'用户名不存在或密码错误'}
    h_pass = user.password
    # 密码错误
    if not check_password_hash(h_pass, password):
        return {'error':'用户名不存在或密码错误'}
    # 一切正常
    else:
        return user.to_dict()


def post_thread(uid, nid, title, content):
    """发帖"""
    if not uid and nid and title and content:
        return {"error":"信息不全"}

    thread = Thread(title, uid, nid, content)
    db.session.add(thread)
    db.session.commit()
    return {'success':'success'}


def post_comment(uid, tid, content):
    """评论"""
    if not uid and tid and content:
        return {"error":"信息不全"}
    
    floor = Comment.query.filter_by(tid=tid).count()+1
    comment = Comment(content, uid, tid, floor)

    db.session.add(comment)
    db.session.commit()
    return {'success':'success'}


def vote_thread(uid, tid, is_up):
    """给帖子投票"""
    vote_thread = VoteThread.query.filter_by(uid=uid, tid=tid).first()
    up = 1 if is_up == True else -1

    if not vote_thread: # 没有点过
        vote_thread = VoteThread(uid, tid, is_up) 
        db.session.add(vote_thread)
        db.session.commit()
        vote_thread.thread.vote += up
        db.session.commit()
        return {'success':'success'}
    elif vote_thread.is_up == is_up: # 重复投票视作取消
        vote_thread.thread.vote -= up
        db.session.delete(vote_thread)
        db.session.commit()
        return {'success':'success'}
    else: 
        vote_thread.is_up = is_up
        vote_thread.thread.vote += up*2
        db.session.commit()
        return {'success':'success'}


def vote_comment(uid, cid, is_up):
    """给评论投票"""
    vote_comment = VoteComment.query.filter_by(uid=uid, cid=cid).first()
    up = 1 if is_up == True else -1

    if not vote_comment: # 没有点过
        vote_comment = VoteComment(uid, cid, is_up)
        db.session.add(vote_comment)
        db.session.commit()
        vote_comment.comment.vote += up
        db.session.commit()
        return {'success':'success'}
    elif vote_comment.is_up == is_up: # 重复投票视作取消
        vote_comment.comment.vote -= up
        db.session.delete(vote_comment)
        db.session.commit()
        return {'success':'success'}
    else:
        vote_comment.is_up = is_up
        vote_comment.comment.vote += up*2
        db.session.commit()
        return {'success':'success'}


def delete_thread(tid):
    """名为删除,实际是取反(删除和恢复)"""
    thread = Thread.query.get(tid)
    if thread.deleted is True and thread.node.deleted is True:
        return {'error':'帖子所在节点已删除,请先恢复节点'}
    if not thread:
        return {'error':'不存在的'}
    thread.deleted = not thread.deleted
    db.session.commit()
    return {'success':'success'}


def delete_node(nid):
    """名为删除,实际是取反(删除和恢复)"""
    node = Node.query.get(nid)
    if not node:
        return {'error':'不存在的'}
    node.deleted = not node.deleted
    for thread in node.threads: # 节点下所有帖子删除
        thread.deleted = not thread.deleted
    db.session.commit()
    return {'success':'success'}


def delete_comment(cid):
    """名为删除,实际是取反(删除和恢复)"""
    comment = Comment.query.get(cid)
    if not comment:
        return {'error':'不存在的'}
    comment.deleted = not comment.deleted
    db.session.commit()
    return {'success':'success'}


def add_node(name, desc):
    """管理员添加节点"""
    node = Node(name, desc)
    db.session.add(node)
    db.session.commit()
    return {'success':'success'}


def mute_user(uid):
    """禁言和恢复"""
    user = User.query.get(uid)
    if not user or user.rid == Role.ROLE_ADMIN:
        return {'error':'不能禁言管理员'}
    if user.rid == Role.ROLE_MUTE:
        user.rid = Role.ROLE_USER
    elif user.rid == Role.ROLE_USER:
        user.rid = Role.ROLE_MUTE
    db.session.commit()
    return {'success':'success'}
    