from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


class user_account(UserMixin, db.Model):
    __tablename__ = "user_account"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    username = db.Column(
        db.UnicodeText,
        # primary_key=True,
        unique=True,
        nullable=False)
    mail = db.Column(
        db.String(32),
        # primary_key=True,
        unique=True,
        nullable=False)
    password = db.Column(db.String(16), nullable=False)
    phone = db.Column(db.String(11))

    Avatar = db.Column(db.String(256), nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, ori_password):
        self.password = generate_password_hash(ori_password,
                                               method='pbkdf2:md5')

    def check_password(self, for_check):
        return check_password_hash(self.password, for_check)
