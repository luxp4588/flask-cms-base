# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    SubmitField, BooleanField, \
                    SelectMultipleField,widgets,\
                    RadioField, SelectField,TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, \
                               EqualTo, Regexp

class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField("用户名",
                           validators=[DataRequired(message="必须填写用户名"),
                                       Length(min=5,max=15,message="用户名长度6～15")],
                           render_kw={"class":"form-control",
                                      "placeholder":"输入用户名"})
    password = PasswordField('密码',
                           validators=[DataRequired(message="必须填写密码"),
                                       Length(min=5,max=15, message="密码长度6～15")],
                           render_kw={"class":"form-control"})


    submit = SubmitField('',
                         render_kw={"class":"btn btn-default",
                                    "value":"立即登录"})

########################################################
# 注册表单部分
########################################################
from wtforms.validators import ValidationError

########################################################
# 如果要定义一个数值区间的验证器，那么参数就类似：
# def __init__(self, min, max, message)
class BadWords:
    '''
    敏感词检查通用验证器
    '''
    def __init__(self, bad_words, message=None):
        '''
        :param bad_words: 敏感词列表
        :param message: 错误提示
        '''
        self.bad_words = bad_words
        if not message:
            message = "不能包含敏感词"
        self.message = message

    def __call__(self, form, field):
        '''
        __call__方法可以让实例对象可以像函数一样调用
        badwords = BadWords(['admin','kf'], message="敏感了")
        验证调用是通过实例调用: badwords(form, field)，
        好像执行了 badwords.__call__(form，field)方法一样

        :param form: 验证表单对象
        :param field: 验证字段对象
        :return:
        '''
        for word in self.bad_words:
            if field.data.find(word)!= -1:
                raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    name = StringField("真实姓名",
                       validators=[DataRequired(message="真实姓名必填"),
                                   BadWords(['admin','客户服务'], message="不能包含敏感词")
                                   ],
                       render_kw={"class":"form-control"})
    username = StringField("用户名",
                    validators=[DataRequired(message="必须填写用户名"),
                                BadWords(['admin', '客户服务'], message="不能包含敏感词")
                                ],
                       render_kw={"class": "form-control"})

    password = PasswordField('密码',
                       validators=[DataRequired(message="必须提供密码"),
                                   Length(min=6, max=15, message="密码长度在6～15之间")],
                       render_kw={"class": "form-control"})

    confirmpassword = PasswordField("确认密码",
                       validators=[EqualTo("password", message="两次输入密码不等")],
                       render_kw={"class": "form-control"})

    sex = RadioField("选择性别",
                     choices=[("1",'男'), ("0", "女")]
                     )

    like = CheckBoxField("选择爱好",
                         choices=[("钓鱼","钓鱼"),("游泳", "游泳")],
                         render_kw={"class": "checkbox-inline"}  )
    city = SelectField('选择城市', choices=[
        ('010', '北京'),
        ('021', '上海'),
        ('0512', '苏州')

    ], render_kw={"class":"form-control"})

    intro = TextAreaField("简介",

                          render_kw={"class": "form-control"} )
    submit = SubmitField('',
                         render_kw={"class":"btn btn-default",
                                    "value":"立即注册"})

    def validate_username(self, field):
        if field.data.find("admin") != -1:
            raise ValidationError("不能包含敏感字")