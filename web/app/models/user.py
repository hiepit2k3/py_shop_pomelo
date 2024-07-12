from ..db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
