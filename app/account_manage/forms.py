import re
from flask_wtf import FlaskForm
# from wtforms import *
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp


def no_chinese(str):
    for ch in str:
        if u'\u4e00' <= ch and ch <= u'u9fff':
            return False
        return True


def no_space(str):
    if ' ' in str:
        return False
    return True


def no_special(str):
    if '@' in str:
        return False
    return True


class RegisterForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[DataRequired(message="请输入用户名")],  #, no_space no_special
        render_kw={
            'class': 'form-control',
            'maxlength': '20'
        })
    password1 = PasswordField(
        '密码',
        validators=[
            DataRequired(message="请输入密码"),
            Length(min=8, max=20, message="密码必须8~20位")  #,
            #no_space, no_chinese
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '密码长度8~20位',
            'maxlength': '40'
        })
    password2 = PasswordField(
        '重复密码',
        validators=[
            DataRequired(),  # message="再次请输入密码"
            EqualTo('password1', message="两次输入的密码不一致！")
        ],
        render_kw={
            'class': 'form-control',
            # 'placeholder': '密码长度8~20位',
            'maxlength': '40'
        })
    mail = StringField('邮箱',
                       validators=[DataRequired(),
                                   Email(message='非法邮箱格式！')],
                       render_kw={
                           'class': 'form-control',
                           'maxlength': '128'
                       })
    phone = StringField('手机（可选）',
                        validators=[Optional()],
                        render_kw={
                            'class': 'form-control',
                            'maxlength': '20'
                        })
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-primary  btn-learn'
            # 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center'
        })
    major = StringField("专业（可选）",
                        validators=[Optional()],
                        render_kw={
                            'class': 'form-control',
                            'maxlength': '20'
                        })
    age = IntegerField("年龄",
                       validators=[DataRequired()],
                       render_kw={
                           'class': 'form-control',
                           'maxlength': '20'
                       })
    gender = SelectField("性别（可选）",
                         validators=[Optional()],
                         render_kw={
                             'class': 'form-control',
                             'maxlength': '20'
                         },
                         choices=[(1, "男"), (2, "女"), (3, "其他")],
                         default=3,
                         coerce=int)
    hometown = StringField("家乡（可选）",
                           validators=[Optional()],
                           render_kw={
                               'class': 'form-control',
                               'maxlength': '20'
                           })


class LoginForm(FlaskForm):
    useraccount = StringField('用户名/邮箱',
                              validators=[DataRequired()],
                              render_kw={
                                  'class': 'form-control',
                                  'maxlength': '40'
                              })
    password = PasswordField('密码',
                             validators=[DataRequired()],
                             render_kw={
                                 'class': 'form-control',
                                 'placeholder': '密码长度8~20位',
                                 'maxlength': '40'
                             })
    remember_me = BooleanField('记住我')  #, render_kw={'class': 'form-control'})
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary  btn-learn'
            # 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center'
        })
