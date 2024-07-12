from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.user_schema import UserSchema
from app.sql import create_user, get_user_by_username_and_pass
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from exceptions import BadRequestException, ConflictException, InternalServerException


api = Blueprint('main', __name__)
user_schema = UserSchema()

@api.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        data_save = create_user(data)
        result = user_schema.dump(data_save)
        return jsonify(result), 201

    except IntegrityError as ie:
        raise ConflictException("Username already exists")

    except ValueError as ve:
        raise BadRequestException(str(ve))

    except SQLAlchemyError as se:
        raise InternalServerException("Database error")

    except Exception as e:
        raise InternalServerException("An unexpected error occurred")
    
@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        result = get_user_by_username_and_pass(data['username'],data['password'])
        if result.length() > 0:
            response_data = {
                'message': 'Login successful',
                'token':'fdjgfd'
            }
            return  jsonify(response_data),200
    except IntegrityError as ie:
        raise ConflictException("Username already exists")

    except ValueError as ve:
        raise BadRequestException(str(ve))

    except SQLAlchemyError as se:
        raise InternalServerException("Database error")

    except Exception as e:
        raise InternalServerException("An unexpected error occurred")