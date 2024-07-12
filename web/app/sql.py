from app.db import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import generate_password_hash, check_password_hash

def create_user(data):
    try:
        # Generate hashed password
        hashed_password = generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data['username'],
            password=hashed_password,
            fullname=data['fullname'],
            gender=data['gender'],
            country=data['country']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_username_and_pass(username,password):
    user =  User.query.filter_by(username = username).first()
    if user and check_password_hash(user.password == password):
        return user
    else:
        return None
