from app import db
from hashlib import sha256

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(256))
    password = db.Column("password", db.String(256))

    def __init__(self, username):
        self.username = username

    @staticmethod
    def get_by_name(name):
        return (User.query.filter_by(username=name).first())
    
    @staticmethod
    def get_by_id(id):
        return (User.query.get(id))

    def add(self, password):
        if (User.get_by_name(self.username) != None):
            return (False)
        self.password = str(sha256(str(password).encode('utf-8')).digest())
        db.session.add(self)
        db.session.commit()
        return (True)
