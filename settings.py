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
    # ckeditor启用上传csrf保护
    # CKEDITOR_ENABLE_CSRF = True

    #Dropzone配置
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = "image"
    # 自定义上传类型
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    # 使用image对应的值
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .jpg, .pdf, .txt'
    DROPZONE_ENABLE_CSRF = True
    # 上传域名字为upload
    DROPZONE_INPUT_NAME = 'upload'


class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass


config =  {
    'development': DevelopmentConfig,
    'production' : ProductionConfig
}