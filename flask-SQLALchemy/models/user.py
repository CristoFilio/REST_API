from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    access = db.Column(db.Integer)

    def __init__(self, username, password, access):
        self.username = username
        self.password = password
        self.access = access

    @classmethod
    def find_user(cls, username=None, _id=None):
        if username:
            return cls.query.filter_by(username=username).first()
        if _id:
            return cls.query.filter_by(id=_id).first()

    def save_user(self):
        db.session.add(self)
        db.session.commit()

