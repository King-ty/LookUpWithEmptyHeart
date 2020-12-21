from app import db
from app.account_manage.models import user_account


class focus(db.Model):
    __tablename__ = 'focus'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    focuser_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    focusee_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
