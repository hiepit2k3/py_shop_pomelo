from app.db import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import pytz
from .token_service import create_token_with_sql
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from exceptions import ConflictException

def create_user(data):
    try:
        data_sql = create_with_sql(data)
        if not isinstance(data_sql, User):
            raise ValueError("Result data is not a User instance")
        # Nếu result_data là một đối tượng User, tiếp tục các thao tác khác
        access_token = create_access_token(identity=data_sql.id, expires_delta=timedelta(minutes=15)) #thời gian sống 15 phút
        refresh_token = create_refresh_token(identity=data_sql.id, expires_delta=timedelta(days=30)) #thời gian sống 30 ngày
        result = create_token_with_sql(data_sql,refresh_token)
        if not result:
            raise ConflictException("Error create to database")
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return data
    except SQLAlchemyError as e:
        print(f"loi day {e}")
        raise e
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"loi day1 {e}")
        raise e
    

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_username_and_pass(username,password):
    try:
        user =  User.query.filter_by(username = username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15), additional_claims={'role':user.role.name})
            refresh_token = create_refresh_token(identity=user.id ,expires_delta=timedelta(days=30), additional_claims={'role':user.role.name})
            create_token_with_sql(user,refresh_token)
            successful = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return successful
        else:
            return False
    except SQLAlchemyError as sql:
        print("err:",sql) 
        raise sql
    except Exception as e:
        print("loi day",e)
        raise e
    
def create_with_sql(data):
    try:
        # Generate hashed password
        hashed_password = generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data['username'],
            password=hashed_password,
            fullname=data['fullname'],
            gender=data['gender'],
            is_active=data['is_active'],
            role_id=data['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    except Exception as e:
        raise e
    
def find_by_id_user(id):
    try:
        user = find_by_id_user_with_sql(id)
        return user
    except SQLAlchemyError as sql:
        raise sql
    except Exception as ex:
        raise ex
   
@staticmethod 
def find_by_id_user_with_sql(id):
    return User.query.get(id)

def generate_accsse_token_by_refresh(id,role):
    return create_access_token(identity=id,expires_delta=timedelta(minutes=15), additional_claims={'role':role})