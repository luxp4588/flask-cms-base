# -*- coding=utf-8 -*-


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///my.db"
    ALLOW_UPLOAD_TYPE = ["image/jpeg", "image/png","image/gif"]
    SECRET_KEY = "123456"

    #CKEDITOR配置
    CKEDITOR_WIDTH = "\"100%\""
    CKEDITOR_HEIGHT = "600"
    CKEDITOR_FILE_UPLOADER = "upload.ckeditor_upload"
    CKEDITOR_FILE_BROWSER = "upload.ckeditor_browser"

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass


config =  {
    'development': DevelopmentConfig,
    'production' : ProductionConfig
}