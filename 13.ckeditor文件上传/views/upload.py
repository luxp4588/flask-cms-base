# -*- coding=utf-8 -*-
import os
from flask import Blueprint, request, render_template
from flask import current_app
import json

upload_app = Blueprint("upload", __name__)

@upload_app.route("/", methods=['get', 'post'])
def upload():
    if request.method == "POST":
        file_storage_list = request.files.getlist("file")
        message = {"result":"","error":"", "filepath_list":[]}
        for file_storage in file_storage_list:
            # 获得上传数据长度
            if request.content_length > 300000*1000:
                message['result'] = "fail"
                message['error'] = "上传文件太大"
                return json.dumps(message)
            # 任何时候，后端都不要相信前端
            # 的数据检测结果，比如上传类型限制，所有必要的检查都须放在
            # 后端进行检测
            if file_storage.content_type not in \
                    current_app.config['ALLOW_UPLOAD_TYPE']:
                message['result'] = "fail"
                message['error'] = "上传文件类型不对"
                return json.dumps(message)

            # # 使用原名直接保存
            file_path= os.path.join(get_dir(),
                                    create_filename(file_storage.filename))
            try:
                file_storage.save(file_path)
            except Exception as e:
                message = {"result":"fail","error":str(e)}
                return json.dumps(message)
            # [1:]将.static/相对路径转为/static绝对路径
            message['filepath_list'].append(file_path[1:])
        message['result'] = "success"
        return json.dumps(message)

    return render_template("upload/jquery_upload.html")


def get_dir():
    '''
    生成文件存放路径
    :return: 存放文件路径
    '''
    from  datetime import date
    # 上传文件存放路径
    base_path = "./static/uploads/"
    # 根据上传的日期存放
    d = date.today()
    # 生成存储路径
    path = os.path.join(base_path, str(d.year), str(d.month))
    # try:
    #     os.makedirs(path)
    # except:
    #     pass
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_filename(filename):
    '''
    生成随机文件名
    :param filename:
    :return:
    '''
    import  uuid
    ext = os.path.splitext(filename)[1]
    new_file_name = str(uuid.uuid4())+ext
    return new_file_name
