# -*- coding=utf-8 -*-

from flask import request, redirect, url_for, render_template
from libs import db
from models import User
from flask import Blueprint


user_app = Blueprint("user_app", __name__)


@user_app.route("/register", methods=['get','post'])
def register():
    if request.method == "POST":
        realname = request.form['name']
        username = request.form['username']
        password = request.form['password']
        sex      = request.form['sex']
        mylike   = '|'.join(request.form.getlist('like'))
        city     = request.form['city']
        intro    = request.form['intro']
        user = User(realname=realname,
                    username=username,
                    password=password,
                    sex=sex,
                    mylike=mylike,
                    city=city,
                    intro=intro)


        db.session.add(user)
        db.session.commit()

    return render_template("user/register.html")


# 获得用户列表
# 如果用户刚进入列表页是访问http://127.0.0.1/user/list
# 与"/list/<int:page>"不匹配，提供一个默认带有page默认值
# 的路由
@user_app.route("/list/<int:page>", methods=['get', "post"])
@user_app.route("/list", defaults={"page":1},methods=['get', "post"])
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


    return render_template("user/user_list.html", users=users,
                           pageList=pageList
                           )


# 根据用户id删除用户
@user_app.route("/delete/<int:user_id>")
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("userList"))


# 用户信息修改
@user_app.route("/edit/<int:user_id>", methods=['get', 'post'])
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
        return redirect(url_for("user_app.userList"))
    return render_template("user/edit_user.html", user=user)
