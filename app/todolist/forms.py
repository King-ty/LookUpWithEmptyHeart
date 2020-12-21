from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms import SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp
import datetime


class AddForm(FlaskForm):
    title = StringField(
        '标题', render_kw={'class': 'form-control', 'maxlength': '32'})
    event = StringField(
        '内容', render_kw={'class': 'form-control', 'maxlength': '32'})
    date = SelectMultipleField("日期",
                               validators=[Optional()],
                               coerce=int,
                               render_kw={
                                   'class': 'form-control',
                                   'maxlength': '10'
                               })
    year = SelectField("年",
                       validators=[Optional()],
                       render_kw={
                           'class': 'form-control',
                           'maxlength': '10'
                       },
                       choices=[(2020, "2020"), (2021, "2021"), (2022, "2022"), (2023, "2023"), (2024, "2024"), (
                           2025, "2025"), (2026, "2026"), (2027, "2027"), (2028, "2028"), (2029, "2029")],
                       default=1,
                       coerce=int)
    month = SelectField("月",
                        validators=[Optional()],
                        render_kw={
                            'class': 'form-control',
                            'maxlength': '10'
                        },
                        choices=[(0, "选择月份"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (
                            6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12")],
                        default=0,
                        coerce=int)
    day_choices = [(0, "选择日期"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13"), (14, "14"), (15, "15"), (16, "16"), (17, "17"), (18, "18"), (19, "19"), (20, "20"), (21, "21"), (22, "22"), (23, "23"), (24, "24"), (25, "25"), (26, "26"), (27, "27"), (28, "28"), (29, "29"), (30, "30"), (31, "31")]
    day = SelectField("日",
                      validators=[Optional()],
                      render_kw={
                          'class': 'form-control',
                          'maxlength': '10'
                      },
                      choices=day_choices,
                      default=0,
                      coerce=int)
    submit = SubmitField(
        '添加',
        render_kw={'class': 'btn btn-primary'})
