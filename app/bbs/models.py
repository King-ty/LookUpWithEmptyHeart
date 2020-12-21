from app import db
# import sys
from datetime import datetime

# sys.path.append("..")


# 论坛主贴数据表
class bbs_post(db.Model):
    __tablename__ = 'bbs_post'
    __table_args__ = {"useexisting": True}
    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        unique=True,
                        nullable=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user_account.id'),
                        nullable=False)
    username = db.Column(
        db.UnicodeText,
        #  db.ForeignKey('user_account.username'),
        nullable=False)
    time = db.Column(db.DateTime, default=datetime.now, index=True)
    head = db.Column(db.Text, nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    commentnum = db.Column(db.Integer, default=1, nullable=False)


# 论坛跟帖数据表
class bbs_comment(db.Model):
    __tablename__ = 'bbs_comment'
    comment_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True,
                           nullable=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user_account.id'),
                        nullable=False)
    username = db.Column(
        db.UnicodeText,
        #  db.ForeignKey('user_account.username'),
        nullable=False)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('bbs_post.post_id'),
                        nullable=False)
    time = db.Column(db.DateTime, default=datetime.now, index=True)
    body = db.Column(db.UnicodeText, nullable=False)
    position = db.Column(db.Integer, nullable=False)
