# -*- coding=utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect,url_for
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
# 创建数据库对象
# 这里不用传入app实例对象，因为这里尚未创建app实例
db=SQLAlchemy()
csrf = CSRFProtect()
ckeditor = CKEditor()

def login_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if not "user" in session:
            return redirect(url_for("login"))
        else:
            print(func)
            return func(*args, **kwargs)
    return decorator_nest