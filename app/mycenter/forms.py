from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp



class MyCenterEditForm(FlaskForm):
   imagewall1 = FileField('图片墙1', 
                           validators=[Optional()],
                           render_kw={
                              'class':'form-control'
                              
                           })
   imagewall2 = FileField('图片墙2',
                         validators=[Optional()],
                         render_kw={
                              'class':'form-control'
                              
                           })
   imagewall3 = FileField('图片墙3', 
                        validators=[Optional()],
                        render_kw={
                              'class':'form-control'
                              
                           })
   header = FileField('头像', 
                        validators=[Optional()],
                        render_kw={
                              'class':'form-control'
                              
                           })
   majorsub = StringField("专业宣言", 
                        validators=[Optional()],
                        )
   agesub = StringField("年龄心声", 
                        validators=[Optional()],
                        render_kw={
                        'class': 'form-control',
                        'maxlength': '60'
                        })
   hometownsub = StringField("家乡简介", 
                        validators=[Optional()],
                        render_kw={
                        'class': 'form-control',
                        'maxlength': '60'
                        })
   introduction = StringField("个人简介", 
                        validators=[Optional()],
                        render_kw={
                        'class': 'form-control',
                        'maxlength': '60'
                        })
   gender = SelectField("性别",
                     validators=[Optional()],
                     render_kw={
                        'class': 'form-control',
                        'maxlength': '20',
                        'id':'gender'
                     },
                     choices=[(1, "男"), (2, "女"), (3, "其他")],
                     coerce=int)
   age = IntegerField("年龄",
                     validators=[Optional()],
                     render_kw={
                           'class': 'form-control',
                           'maxlength': '20',
                           'id':'age'
                     })
   hometown = StringField("家乡",
                        validators=[Optional()],
                        render_kw={
                           'class': 'form-control',
                           'maxlength': '20'
                        })
   major = StringField("专业",
                        validators=[Optional()],
                        render_kw={
                           'class': 'form-control',
                           'maxlength': '20'
                        })
   submit= SubmitField('提交修改',
                     render_kw={
                        'class': 'form-control'
                        
                     })
   submit_majorsub = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'majorsub'
                     })
   submit_agesub = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'agesub'
                     })
   submit_hometownsub = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'hometownsub'
                     })
   submit_introduction = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'introduction'
                     })
   submit_gender = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'gender'
                     })
   submit_age = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'age'
                     })
   submit_hometown = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'hometown'
                     })
   submit_major = SubmitField('提交修改',
                     render_kw={
                        'class': 'btn btn-primary',
                        'id':'major'
                     })

