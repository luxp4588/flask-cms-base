# -*- coding=utf-8 -*-


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///my.db"
    ALLOW_UPLOAD_TYPE = ["image/jpeg", "image/png","image/gif"]
    SECRET_KEY = "123456"

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass


config =  {
    'development': DevelopmentConfig,
    'production' : ProductionConfig
}