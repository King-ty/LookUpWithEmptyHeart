from app import db, app
from config import Config
from flask_login import UserMixin
from app.account_manage import models
from app.chatroom import models
from app.focus_manage import models
from app.bbs import models
from app.myblog import models
from app.mycenter import models
from app.todolist import models

db.create_all()
