# -*- coding=utf-8 -*-

from flask import request,session,render_template,\
                  redirect, url_for

from .admin_app import admin_app
from models import Article,Category
from libs import db
import json

@admin_app.route("/article/post", methods=['get','post'])
def article_post():
    if request.method == "POST":
        cate_id = request.form['cate']
        title = request.form['title']
        intro    = request.form['intro']
        content  = request.form['content']
        article = Article(
                    cate_id = cate_id,
                    title=title,
                    intro=intro,
                    content=content,
                    author=session['user']
         )


        db.session.add(article)
        db.session.commit()
        message = {"message":"发布成功"}
        return json.dumps(message)

    return render_template("admin/article/article_post.html")


# 获得文章列表
@admin_app.route("/article/list/<int:page>", methods=['get', "post"])
@admin_app.route("/article/list", defaults={"page":1},methods=['get', "post"])
def article_list(page):
    if request.method == "POST":
        q = request.form['q']
        condition = {request.form['field']:q}
        if request.form['field'] == "title":
            condition = Article.title.like('%%%s%%' % q)
        else:
            condition = Article.content.like('%%%s%%' % q)
        if request.form['order'] == "1":
            order = Article.id.asc()
        else:
            order = Article.id.desc()

        res = Article.query.filter(condition)\
                                .order_by(order)\
                                .paginate(page, 10)


    else:
        res = Article.query.paginate(page,10)

    # 无论搜索还是默认查看，都是翻页处理
    articles = res.items
    pageList = res.iter_pages()


    return render_template("admin/article/article_list.html", articles=articles,
                           pageList=pageList
                           )


# 根据文章id删除文章
@admin_app.route("/article/delete/<int:article_id>")
def article_delete(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for(".article_list"))


# 文章修改
@admin_app.route("/article/edit/<int:article_id>", methods=['get', 'post'])
def article_edit(article_id):
    article = Article.query.get(article_id)
    if request.method == "POST":
        article.cate_id = request.form['cate']
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.content= request.form['content']
        db.session.commit()
        return redirect(url_for(".article_list"))
    return render_template("admin/article/article_edit.html", article=article)
