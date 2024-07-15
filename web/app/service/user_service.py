from app.db import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import pytz
from .token_service import create_token_with_sql

SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

def create_user(data):
    try:
        result_data = create_with_sql(data)
        if not isinstance(result_data, User):
            raise ValueError("Result data is not a User instance")
        # Nếu result_data là một đối tượng User, tiếp tục các thao tác khác
        access_token = create_access_token(result_data)
        refresh_token = create_refresh_token(result_data)
        
        result =  create_token_with_sql(result_data,access_token,refresh_token)
        return result
    except SQLAlchemyError as e:
        raise e
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise e
    

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_username_and_pass(username,password):
    try:
        user =  User.query.filter_by(username = username).first()
        # print(check_password_hash(user.password, password))
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
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
        print("loi",e)
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
    
def create_access_token(user_data):
    try:
        # print('toke')
        payload = {
            'user_id': user_data.id,
            'username': user_data.username,
            'exp': datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')) + timedelta(minutes=15)  # Token hết hạn sau 15 phút
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as a:
        return a

def create_refresh_token(user_data):
    payload = {
        'user_id': user_data.id,
        'username': user_data.username,
        'exp': datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')) + timedelta(days=30)  # Token hết hạn sau 30 ngày
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token đã hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ
    
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