from app import db
import sys
from datetime import datetime

sys.path.append("..")

# 博客数据表
class myblog_info(db.Model):
    __tablename__ = 'myblog_info'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    time=db.Column(db.DateTime, default=datetime.now, index=True)
    head=db.Column(db.Unicode(30),nullable=False)
    body=db.Column(db.UnicodeText,nullable=False)
    openstate=db.Column(db.Boolean,default=False, nullable=False) #是否将博客中的文本内容同步至论坛
    likenum=db.Column(db.Integer, default=0, nullable=False)      #点赞数
    # 加入图片功能: 图片数[0, 3]
    imgnum=db.Column(db.Integer, default=0, nullable=False)
    img1=db.Column(db.String(80), nullable=True)
    img2=db.Column(db.String(80), nullable=True)
    img3=db.Column(db.String(80), nullable=True)




