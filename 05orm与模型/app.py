from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"

db=SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html" )


@app.route('/login', methods=['get', 'post'])
def login():
    # username = request.args.get("username")
    # password = request.args.get("password")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)
    return render_template("login.html")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city = db.Column(db.String)
    intro = db.Column(db.String)

@app.route("/register", methods=['get','post'])
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

    return render_template("register.html")


@app.context_processor
def account():
    username = None
    return {"username":username}