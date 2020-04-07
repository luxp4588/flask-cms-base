# -*- coding=utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

# 创建数据库对象
# 这里不用传入app实例对象，因为这里尚未创建app实例
db=SQLAlchemy()