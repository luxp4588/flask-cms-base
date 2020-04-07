# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    SubmitField, BooleanField, \
                    SelectMultipleField,widgets,\
                    RadioField, SelectField,TextAreaField
from flask_ckeditor import CKEditorField

class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField("用户名",
                           render_kw={"class":"form-control",
                                      "placeholder":"输入用户名"})
    password = PasswordField('密码',
                             render_kw={"class":"form-control"})

    # 多选框选项
    # choices = [(1,"一周免登录"),(2,"二周免登录"),(3,"三周免登录")]
    # remember = CheckBoxField("记忆方式", choices=choices)

    submit = SubmitField('',
                         render_kw={"class":"btn btn-default",
                                    "value":"立即登录"})



class RegisterForm(FlaskForm):
    name = StringField("真实姓名",
                       render_kw={"class":"form-control"})
    username = StringField("用户名",
                       render_kw={"class": "form-control"})

    password = PasswordField('密码',
                       render_kw={"class": "form-control"})

    confirmpassword = PasswordField("确认密码",
                       render_kw={"class": "form-control"})

    sex = RadioField("选择性别",
                     choices=[(1,'男'), (0, "女")]
                     )

    like = CheckBoxField("选择爱好",
                         choices=[(1,"钓鱼"),(2, "游泳")],
                         render_kw={"class": "checkbox-inline"}  )
    city = SelectField('选择城市', choices=[
        ('010', '北京'),
        ('021', '上海'),
        ('0512', '苏州'),

    ], render_kw={"class":"form-control"})
    # 如果这里使用
    # intro = CKEditorField("简介")
    # 输出的textarea中带有class="ckeditor"
    # ckeditor会自动在带有class="ckeditor"的字段上创建富文本编辑器，而不需要
    # 通过{{ ckeditor.config() }}来设置
    intro = TextAreaField("简介")
    submit = SubmitField('',
                         render_kw={"class":"btn btn-default",
                                    "value":"立即注册"})
