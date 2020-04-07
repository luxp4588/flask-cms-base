from flask import Flask, render_template
from flask import request, redirect, url_for
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
    username = request.args.get("username")
    password = request.args.get("password")
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


# 获得用户列表
@app.route("/userlist", methods=['get', "post"])
def userList():
    '''
     当搜索表单的method是post的时候，翻页之后，搜索的条件会丢失
     必须在搜索的链接中加上 ?q=搜索词&field=搜索字段&order=排序类型&page=page
     比如: /userlist?q=luxp&field=username&order=1&page=2
     修改方法:
       修改模版中搜索表单的methos属性为get，即表单提交方式改为get，这时候提交搜索可以发现地址栏中包含搜索
       这种方式接受参数不能使用request.form，必须使用requst.args.get的方式接受数据
       参考 userList2
    '''
    if request.method == "POST":
        q = request.form['q']

        # 使用filter_by
        # condition = {request.form['field']: q}
        # users = User.query.filter_by(**condition).all()

        # 使用filter可以使用like模糊查询
        # 举例: 比如 like '%luxp%',表示包含luxp的都可以，"yluxpz","aluxpb".....

        if request.form['field'] == "realname":
            condition = User.realname.like('%%%s%%' % q)
        else:
            condition = User.username.like('%%%s%%' % q)
        if request.form['order'] == "1":
            order = User.id.asc()
        else:
            order = User.id.desc()

        users = User.query.filter(condition, User.sex==request.form['sex']).order_by(order).all()

    else:
        # users = User.query.all()
        page = request.args.get('page',1)
        users = User.query.paginate(int(page),10)


    return render_template("user/user_list.html", users=users.items,
                           pages=users.pages,
                           total=users.total,
                           pageList=users.iter_pages()
                           )


# 获得用户列表
@app.route("/userlist2", methods=['get'])
def userList2():
    '''
      需要将method修改为get
      翻页后，搜索条件不会丢失

    :return:
    '''
    # 默认页号为1
    page = request.args.get('page', 1)

    # 如果提交了查询关键词q
    q = request.args.get('q')
    if q:
        field = request.args.get('field')
        print(field)
        if field == "realname":
            condition = User.realname.like('%%%s%%' % q)
        else:
            condition = User.username.like('%%%s%%' % q)

        order_type = request.args.get('order')
        if  order_type == "1":
            order = User.id.asc()
        else:
            order = User.id.desc()

        sex = request.args.get('sex',1)
        users = User.query.filter(condition, User.sex ==sex ).order_by(order).paginate(int(page), 10)
        # 拼接查询条件（相当于request的query_string属性）
        # 在模版的翻页部分添加上query_string
        query_string = "q=" + q + "&field=" + field + "&sex=" + sex+ "&order=" + order_type
    else:
        users = User.query.paginate(int(page), 10)
        query_string = ""
    print(query_string)
    return render_template("user/user_list.html", users=users.items,
                           pages=users.pages,
                           total=users.total,
                           pageList=users.iter_pages(),
                           condition=query_string
                           )


# 根据用户id删除用户
@app.route("/user_delete/<int:user_id>")
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("userList"))


# 用户信息修改
@app.route("/useredit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.mylike = "|".join(request.form.getlist('like'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for("userList"))
    return render_template("user/edit_user.html", user=user)


def createBatchUsers():
    words = list("abcdefghijklmnopqrstuvwxyz")
    citys = ["010", "021", "0512"]
    mylikes = ["睡觉","旅游", "看书", "唱歌"]
    import random

    for i in range(100):
        random.shuffle(words)
        username = "".join(words[:6])
        sex = random.randint(0,1)
        city = citys[random.randint(0,2)]
        random.shuffle(mylikes)
        mylike = "|".join(mylikes[:random.randint(0,3)])
        user = User(realname="-",
                    username=username,
                    password="",
                    sex=sex,
                    mylike=mylike,
                    city=city,
                    intro="")
        db.session.add(user)
    db.session.commit()