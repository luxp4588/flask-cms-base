# -*- coding=utf-8 -*-

import json
from flask import request,session,render_template,\
                  redirect, url_for

from .admin_app import admin_app
from models import User
from libs import db, csrf
import json


@admin_app.route("/user/list/<int:page>", methods=['get', "post"])
@admin_app.route("/user/list", defaults={"page":1},methods=['get', "post"])
def userList(page):
    if request.method == "POST":
        q = request.form['q']
        condition = {request.form['field']:q}
        #filter_by
        # users = User.query.filter_by(**condition).all()
        # filter
        # like
        if request.form['field'] == "realname":
            condition = User.realname.like('%%%s%%' % q)
        else:
            condition = User.username.like('%%%s%%' % q)
        if request.form['order'] == "1":
            order = User.id.asc()
        else:
            order = User.id.desc()

        res = User.query.filter(condition,
                                User.sex==request.form['sex'])\
                                .order_by(order)\
                                .paginate(page, 10)


    else:
        # users = User.query.all()

        res = User.query.paginate(page,10)
    # 无论搜索还是默认查看，都是翻页处理
    users = res.items
    pageList = res.iter_pages()


    return render_template("admin/user/user_list.html", users=users,
                           pageList=pageList, pages=res.pages,
                           total=res.total
                           )


# 根据用户id删除用户
@admin_app.route("/user/delete", methods=['post'])
def deleteUser():
    csrf.protect()
    user_id = int(request.form.get("user_id"))
    user = User.query.get(user_id)
    message = {}
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        message['result'] = "fail"
    else:
        message['result'] = "success"
    return json.dumps(message)


# 用户信息修改
@admin_app.route("/user/edit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.mylike = "|".join(request.form.getlist('like'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for(".userList"))
    return render_template("admin/user/user_edit.html", user=user)
