from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp


class AddPostForm(FlaskForm):
    topic = StringField('主题',
                        validators=[
                            DataRequired(message="未输入主题"),
                            Length(min=1, max=100, message="长度应为1~100个字符")
                        ],
                        render_kw={
                            'placeholder': '在这里输入主题，不得超过100个字符',
                            'class': 'form_control',
                            'maxlength': '100'
                        })
    content = TextAreaField('内容',
                            validators=[
                                DataRequired(message='未输入内容'),
                                Length(min=1,
                                       max=10000,
                                       message='长度应为1~10000字符')
                            ],
                            render_kw={
                                'rows': '10',
                                'placeholder': '在这里输入内容，不得超过10000个字符',
                                'class': 'form_control',
                                'maxlength': 10000
                            })
    submit = SubmitField(
        '发起讨论',
        render_kw={'class': 'center btn btn-primary d-block mt-2 px-5'})


class AddCommentForm(FlaskForm):
    comment = TextAreaField('添加评论',
                            validators=[
                                DataRequired(message='未输入内容'),
                                Length(min=1, max=600, message="长度应为1~600个字符")
                            ],
                            render_kw={
                                "rows": '5',
                                "placeholder": "这里输入评论内容，不得超过600个字符",
                                'maxlength': '600'
                            })
    submitComment = SubmitField('发表评论')


class EditDeleteForm(FlaskForm):
    submitEdit = SubmitField(
        '编辑', render_kw={'class': 'center btn btn-primary d-block mt-2 px-3'})
    submitDelete = SubmitField(
        '删除', render_kw={'class': 'center btn btn-primary d-block mt-2 px-3'})
