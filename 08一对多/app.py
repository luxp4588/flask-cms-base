from flask import Flask, render_template
from flask import request, redirect, url_for
from libs import db
from views.users import user_app
from views.articles import article_app
from flask_migrate import Migrate
from models import Category


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"

db.init_app(app)

app.register_blueprint(user_app, url_prefix="/user")
app.register_blueprint(article_app, url_prefix="/article")

@app.route('/')
def index():
    return render_template("index.html" )

#
@app.route('/login', methods=['get', 'post'])
def login():
    # username = request.args.get("username")
    # password = request.args.get("password")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)
    return render_template("login.html")




@app.context_processor
def account():
    username = None
    return {"username":username}

@app.context_processor
def getCateList():
    cates = Category.query.all()
    return {"cates":cates}

# 添加render_as_batch=True
# SQLite支持批处理修改
# 但是这种如果修改多个字段，可能在发生错误时，发生修改不一致
migrate = Migrate(app,db,render_as_batch=True)