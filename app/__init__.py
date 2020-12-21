# -*- coding: utf-8 -*-
# import os
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  ##
from flask_bootstrap import Bootstrap
from config import Config  # settings.py改为config.py
# from .models import *

app = Flask(__name__)

app.config.from_object(Config)  # from_myprofile改为from_object
app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)  #从本地加载bootstrap##

app.jinja_env.trim_blocks = True  ##
app.jinja_env.lstrip_blocks = True  ##

db = SQLAlchemy(app)
db.init_app(app)
# db.create_all()
migrate = Migrate(app, db)
login = LoginManager(app)  ##
login.init_app(app)
login.login_message = u'请先登录！'
login.login_view = 'account.login'

bootstrap = Bootstrap(app)

# 必须放在app定义之后，因为.views要import .app
# from .models import *
# @app.route('/')
# def html_signup_index():
#     return render_template('signup_index.html')

# views中已经导入了models，否则此处需import .models
# db.create_all要在models定义完成之后，否则无法导入表
# 因此，建议不要在这里create_all，而是运行主文件夹中的db_create.py
# db.create_all()
