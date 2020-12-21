from app import db


# 个人中心信息数据库
class MycenterInfo(db.Model):
    __tablename__ = 'MycenterInfo'
    id = db.Column(db.Integer,
                   db.ForeignKey('user_account.id'),
                   primary_key=True)
    name = db.Column(db.Unicode(10))
    gender = db.Column(db.String(8), nullable=True)
    gendersubintro = db.Column(db.UnicodeText, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    agesubintro = db.Column(db.UnicodeText, nullable=True)
    hometown = db.Column(db.Unicode(20), nullable=True)
    hometownsubintro = db.Column(db.UnicodeText, nullable=True)
    major = db.Column(db.UnicodeText, nullable=True)
    majorsubintro = db.Column(db.UnicodeText, nullable=True)
    introduction = db.Column(db.UnicodeText, nullable=True)
    picture1 = db.Column(db.String(80), nullable=True)
    picture2 = db.Column(db.String(80), nullable=True)
    picture3 = db.Column(db.String(80), nullable=True)
    header = db.Column(db.String(80), nullable=True)
