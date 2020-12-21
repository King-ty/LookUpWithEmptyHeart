from app import db
# import sys
from datetime import datetime

# sys.path.append("..")


class chat_message(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    sender_id = db.Column(db.Integer,db.ForeignKey('user_account.id'))
    receiver_id = db.Column(db.Integer,db.ForeignKey('user_account.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    text = db.Column(db.UnicodeText, nullable=False)
