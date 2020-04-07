# -*- coding=utf-8 -*-

from flask import request, redirect, url_for, render_template
from libs import db, login_required
from models import User
from flask import Blueprint
from forms.account_form import RegisterForm

user_app = Blueprint("user_app", __name__)


@user_app.route("/register", methods=['get','post'])
def register():
    form = RegisterForm()
    message= None
    # if request.method == "POST":
    if form.validate_on_submit():
        if validate_username(form.data['username']):
            return render_template("user/register.html",
                                   message="用户名重复")

        realname = form.data['name']
        username = form.data['username']
        password = form.data['password']
        sex = form.data['sex']
        mylike   = '|'.join(form.data['like'])
        city     = form.data['city']
        intro    = form.data['intro']
        user = User(realname=realname,
                    username=username,
                    sex=sex,
                    mylike=mylike,
                    city=city,
                    intro=intro)
        # 密码加密
        user.hash_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception as e:
            message = "注册失败:" + str(e)
    else:
        print(form.errors)
    return render_template("user/register.html", message=message, form=form)

# 验证用户名是否重复
def validate_username(username):
    return User.query.filter_by(username=username).first()



