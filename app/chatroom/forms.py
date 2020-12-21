from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp

class ChatroomForm(FlaskForm):
    msg_text = StringField(validators=[DataRequired(message="在此输入消息"),Length(min=1, max=100, message="不超过50字")])
    send = SubmitField('发送')