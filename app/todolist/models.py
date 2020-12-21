from app import db


class todolist_list(db.Model):
    __tablename__ = "todolist_list"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    userid_id = db.Column(db.Integer)
    title = db.Column(db.Unicode(32))
    event = db.Column(db.Unicode(255), nullable=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)