# -*- coding=utf-8 -*-
from libs import db
from models import User


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