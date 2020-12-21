from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp, InputRequired

class MyblogEditForm(FlaskForm):
    head=StringField(u"博客标题", 
        validators=[
            Length(min=1, max=50, message=u"标题不能超过25字"),
            DataRequired(message="未输入标题")
        ],
        render_kw={
            'placeholder': '在这里输入主题，不得超过100个字符',
            'class': 'form-control',
            'maxlength': '100'
        }
    )
    body=TextAreaField(label=u"博客",
        validators=[
            Length(min=1, max=2000, message=u"内容不能超过1000字"),
            DataRequired(message="未输入内容")
        ],
        render_kw={
            'placeholder':'这里输入博客内容，不超过1000字',
            'class':'form-control row',
            'rows':'12',
            "cols":'20',
            'maxlength':'2000'
        }
    )
    openstate=BooleanField(label=u"同步至论坛帖子",
        validators=[Optional()] 
    )
    img1=FileField(u"博客图片1",
        validators=[Optional()],
        render_kw={
            'class':'form-control'
        })
    img2=FileField(u"博客图片2",
        validators=[Optional()],
        render_kw={
            'class':'form-control'
        })
    img3=FileField(u"博客图片3",
        validators=[Optional()],
        render_kw={
            'class':'form-control'
        })
    submit=SubmitField("提交",
                    validators=[Optional()],
                    render_kw={
                    'class': 'btn btn-primary'
                    })

