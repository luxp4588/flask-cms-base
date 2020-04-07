# -*- coding=utf-8 -*-

from flask import request, redirect, url_for, render_template
from libs import db, login_required
from models import Article, Category
from flask import Blueprint


article_app = Blueprint("article_app", __name__)

# 根据文章id阅读文章
@article_app.route("/view/<int:article_id>")
def view(article_id):
    article = Article.query.get(article_id)
    if  not article:
        return redirect(url_for(".list"))
    return render_template("article/detail.html", article=article)


# 根据文章cate_id显示文章列表
@article_app.route("/cate/<int:cate_id>/<int:page>")
@article_app.route("/", defaults={"cate_id":0, "page":1})
def getArticleList(cate_id, page):
    if cate_id == 0:
        res = Article.query.paginate(page, 20)
    else:
        res = Article.query.filter_by(cate_id=cate_id).paginate(page,20)
    articles = res.items
    pageList = res.iter_pages()
    return render_template("index.html",
                            articles=articles,
                            pageList=pageList
                           )



