# -*- coding:utf-8 -*-
"""views.py  page views"""
from flask import render_template, json, session, redirect, request, abort
from cyanit import app, db
from functools import wraps
from .controllers import *


def admin_required(f):
    """需要管理员权限"""
    @wraps(f)
    def decorator(*args, **kwargs):
        user = session.get('user')
        if user and user.get('role')=='admin':
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator


########################### 页面 ####################################
@app.errorhandler(403)
def page_forbidden(e):
    """403自定义"""
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    """404自定义"""
    return render_template('404.html'), 404


@app.route('/')
@app.route('/welcome')
def welcome():
    """欢迎页面"""
    return render_template("welcome.html")


@app.route('/index')
def index():
    """主页"""
    user = session.get('user')
    nodes = get_all_nodes()
    # nodes = filter_deleted(nodes)

    if user:
        # 用户身份，可能发送post用来发帖
        threads = get_all_threads_with_vote(user.get('id'))
        # threads = filter_deleted(threads)
        return render_template("index.html", threads=threads, user=user, nodes=nodes)
    else:
        threads = get_all_threads()
        # threads = filter_deleted(threads)
        # 游客身份，可能发送post用来登录
        return render_template("index.html", threads=threads)


@app.route('/admin/<mtype>')
@admin_required
def manage_page(mtype):
    """后台管理页面"""
    user = session.get('user')
    if mtype == "thread":
        threads = get_all_threads()
        return render_template("admin/manage-%s.html" % mtype, user=user, threads=threads)
    elif mtype == "user":
        users = get_all_users()
        return render_template("admin/manage-%s.html" % mtype, user=user, users=users)
    elif mtype == "node":
        nodes = get_all_nodes()
        return render_template("admin/manage-%s.html" % mtype, user=user, nodes=nodes)
    elif mtype == "comment":
        comments = get_all_comments()
        return render_template("admin/manage-%s.html" % mtype, user=user, comments=comments)
    else:
        abort(404)


@app.route('/user/mute', methods=['POST'])
@admin_required
def api_mute():
    """禁言某人"""
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        abort(403)

    uid = request.form.get('id')
    res = mute_user(uid)
    return json.dumps(res)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    if request.method == 'GET':
        return render_template("user/register.html")
    else:
        name = request.form['username']
        email = request.form['email']
        passwd = request.form['password']
        p_confirm = request.form['password_confirm']
        res = do_register(name, email, passwd, p_confirm)
        return json.dumps(res)


@app.route('/login', methods=['POST'])
def login():
    """登录,检查用户名密码"""
    name = request.form['username']
    password = request.form['password']
    res = do_login(name, password)
    if 'error' in res.keys():
        return json.dumps(res)
    else:
        session['user'] = res
        return json.dumps({'success':'success'})


@app.route('/logout')
def logout():
    """登出，清空session"""
    session.pop('user', None)
    return redirect('/index')


@app.route('/node')
def show_all_node():
    """显示所有的节点"""
    user = session.get('user')
    nodes = get_all_nodes()
    # nodes = filter_deleted(nodes)
    return render_template("node/show_node.html", user=user, nodes=nodes)


@app.route('/node/<name>')
def show_node_thread(name):
    """只显示某个节点的帖子"""
    user = session.get('user')
    nodes = get_all_nodes()
    thisnode = {}
    for node in nodes:
        if node['name'] == name:
            thisnode = node
    if not thisnode or thisnode.get('deleted'):
        abort(404)

    if user:
        # 用户身份，可能发送post用来发帖
        threads = get_threads_by_nid_with_vote(thisnode['id'], user["id"])
        return render_template("node/node_detail.html", threads=threads, user=user, nodes=nodes, thisnode=thisnode)
    else:
        # 游客身份，可能发送post用来登录
        threads = get_threads_by_nid(thisnode['id'])
        return render_template("node/node_detail.html", threads=threads, thisnode=thisnode)


@app.route('/node/nsfw')
def nsfw():
    """not suitable for work"""
    return "You bad bad!"


@app.route('/node/add', methods=['POST'])
@admin_required
def api_add_node():
    """添加节点"""
    name = request.form['name']
    desc = request.form['desc']
    res = add_node(name, desc)
    return json.dumps(res)


@app.route('/node/delete', methods=['POST'])
@admin_required
def api_del_node():
    """删除节点"""
    nid = request.form['id']
    res = delete_node(nid)
    return json.dumps(res)


@app.route('/thread', methods=['POST'])
def api_post_thread():
    """发帖"""
    user = session.get('user')
    uid = user.get('id')
    if user.get('role') == 'mute':
        return json.dumps({'error':'您已被禁言!'})
    title = request.form['title']
    content = request.form['content']
    nid = request.form['node']
    res = post_thread(uid, nid, title, content)
    return json.dumps(res)


@app.route('/thread/<int:tid>')
def thread_detail(tid):
    """帖子页"""
    user = session.get('user')
    thread = get_thread_by_tid(tid)
    if not thread or thread.get('deleted'):
        return render_template('404.html'), 404

    if user: # 登录后增加用户的投票记录
        vote_status = VoteThread.query.filter_by(tid=tid, uid=user['id']).first()
        if vote_status:
            thread['vstatus'] = vote_status.is_up
        comments = get_comments_by_tid_with_vote(tid, user['id'])
    else:
        comments = get_comments_by_tid(tid)
    return render_template("thread/thread_detail.html", user=user, comments=comments, thread=thread)


#example: /thread/vote/2?action=down
@app.route('/thread/vote/<int:tid>', methods=['POST'])
def api_vote_thread(tid):
    """给帖子投票"""
    uid = session['user']['id']
    action = request.args.get('action')
    if action != 'up' and action != 'down':
        return json.dumps({'error':'error'})
    else:
        is_up = True if action == 'up' else False
        res = vote_thread(uid, tid, is_up)
        return json.dumps(res)


@app.route('/thread/delete', methods=['POST'])
def api_del_thread():
    """删帖"""
    tid = request.form.get('id')
    res = delete_thread(tid)
    return json.dumps(res)


@app.route('/comment/<int:tid>', methods=['POST'])
def api_comment(tid):
    """评论"""
    user = session.get('user')
    uid = user.get('id')
    if user.get('role') == 'mute':
        return json.dumps({'error':'您已被禁言!'})
    content = request.form['content']
    res = post_comment(uid, tid, content)
    return json.dumps(res)


#example: /comment/vote/2?action=up
@app.route('/comment/vote/<int:cid>', methods=['POST'])
def api_vote_comment(cid):
    """给评论投票"""
    user = session.get('user')
    uid = user.get('id')
    action = request.args.get('action')
    if action != 'up' and action != 'down':
        return json.dumps({'error':'error'})
    else:
        is_up = True if action == 'up' else False
        res = vote_comment(uid, cid, is_up)
        return json.dumps(res)


@app.route('/comment/delete', methods=['POST'])
@admin_required
def api_del_comment():
    """删除评论"""
    cid = request.form.get('id')
    res = delete_comment(cid)
    return json.dumps(res)
