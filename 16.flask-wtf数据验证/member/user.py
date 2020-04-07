# -*- coding=utf-8 -*-

from flask import request,session,render_template,\
                  redirect, url_for

from .member_app import member_app
from models import User
from libs import db
import json


# 用户信息修改
@member_app.route("/user/edit", methods=['get', 'post'])
def userEdit():
    # 普通会员只能修改自己的资料
    # 修改资料的时候还需要验证密码
    user = User.query.filter_by(username=session['user']).one()
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.mylike = "|".join(request.form.getlist('like'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
    return render_template("member/info/info_edit.html", user=user)
