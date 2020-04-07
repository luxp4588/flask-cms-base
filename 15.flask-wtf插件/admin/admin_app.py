# -*- coding=utf-8 -*-

from flask import request, session, redirect, url_for,\
                  render_template
from flask import Blueprint
from libs import login_required


admin_app = Blueprint("admin_app", __name__)

@admin_app.before_request
@login_required
def is_admin():
    print(session['user'])
    if session['user'] != "admin":
        return redirect(url_for("login"))


@admin_app.route("/")
def admin_index():
    return render_template("admin/admin_index.html")