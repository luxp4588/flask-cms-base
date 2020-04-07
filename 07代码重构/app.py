from flask import Flask, render_template
from flask import request, redirect, url_for
from libs import db
from views.users import user_app
from views.articles import article_app
from flask_migrate import Migrate

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




migrate = Migrate(app,db)