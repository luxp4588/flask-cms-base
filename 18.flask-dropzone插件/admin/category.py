# -*- coding=utf-8 -*-

from flask import request,session,render_template,\
                  redirect, url_for

from .admin_app import admin_app
from models import Article,Category
from libs import db
import json


# 分类视图部分
# 添加分类
@admin_app.route("/category/add_cate", methods=['get','post'])
def addCate():
    message = None
    if request.method == "POST":
        cate_name = request.form['name']
        cate_order    = request.form['order']
        category = Category(
                    cate_name=cate_name,
                    cate_order=cate_order,
         )
        try:
            db.session.add(category)
            db.session.commit()
            message = cate_name+"添加成功"
        except Exception as e:
            message = "发生了错误:" + str(e)
            # 如果插入失败，进行回滚操作
            db.session.rollback()

    return render_template("admin/category/category_add.html", message=message)


# 获得分类列表
@admin_app.route("/category/cate_list")
def cateList():

    cates = Category.query.order_by(Category.cate_order.desc()).all()
    return render_template("admin/category/category_list.html", cates=cates )


# 删除分类
@admin_app.route("/category/cate_delete/<int:cate_id>")
def deleteCate(cate_id):
    cate = Category.query.get(cate_id)
    db.session.delete(cate)
    db.session.commit()
    return redirect(url_for(".cateList"))


# 分类修改
@admin_app.route("/cate_edit/<int:cate_id>", methods=['get', 'post'])
def editCate(cate_id):
    category = Category.query.get(cate_id)
    if request.method == "POST":
        category.cate_name = request.form['name']
        category.cate_order = request.form['order']
        db.session.commit()
        return redirect(url_for(".cateList"))
    return render_template("category/edit.html", category=category)


