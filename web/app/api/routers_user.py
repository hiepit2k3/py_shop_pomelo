from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.role import Role
from ..models.schema.user_schema import UserSchema
from ..models.schema.token_schama import Tokenschema
from app.service.user_service import create_user, get_user_by_username_and_pass,find_by_id_user, generate_accsse_token_by_refresh
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from exceptions import BadRequestException, ConflictException, InternalServerException, InvalidCredentialsException, NotFoundException
from ..service.role_service import create_with_sql
from ..utils.response import CustomResponse
from exceptions import CustomAPIException
from ..auth import token_required,role_required
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token, get_jwt


api = Blueprint('main', __name__)
user_schema = UserSchema()
token_schema = Tokenschema()


# Register new account 
@api.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        data_save = create_user(data)
        if not data:
            raise ValueError("No input data provided")
        result = token_schema.dump(data_save)
        response = CustomResponse(data=result)
        return jsonify(response.to_dict()), 201
    except IntegrityError as ie:
        raise ConflictException("Username already exists")
    except ValueError as ve:
        raise BadRequestException(str(ve))
    except SQLAlchemyError as se:
        raise InternalServerException("Database error")
    except Exception as e:
        print(f"loi {e}")
        raise InternalServerException("An unexpected error occurred")

# Login account by username and password
@api.route('/login', methods=['POST'])
def login():
    try:
        print("dhkdshkfhkhd")
        data = request.get_json()
        print(data['username'])
        result = get_user_by_username_and_pass(data['username'],data['password'])
        if not result:
            raise InvalidCredentialsException("Username or password incorect, Please input again!")
        respone = CustomResponse(data=result,status_code=200)
        return jsonify(respone.to_dict()), 200
    except IntegrityError as ie:
        raise ConflictException("Username already exists")
    except ValueError as ve:
        raise BadRequestException(str(ve))
    except SQLAlchemyError as se:
        raise InternalServerException("Database error")
    except Exception as ex:
        print("dfjgksdfjss",ex)
        raise ex

# Create role new with role admin
@api.route('/role/register', methods=['POST'])
# @jwt_required()
# @token_required
# @role_required('admin')
def create_role():
    try:
        data = request.get_json()
        result = create_with_sql(data)
        if not isinstance(result, Role):
            raise InternalServerException("new add fail!")
        respon = CustomResponse(data={"message":"add new role successfully!"})
        return jsonify(respon.to_dict()), 201
    except ValueError as ve:
        raise BadRequestException(str(ve))
    except SQLAlchemyError as se:
        raise InternalServerException("Database error")
    except CustomAPIException as ex:
        raise ex
    except Exception as e:
        raise InternalServerException("An unexpected error occurred")

# Find imformation user by id 
@api.route('/user/find/<int:user_id>', methods=['GET'])
@jwt_required()
@token_required
def find_by_id_user_route(user_id):
    try:
        print(user_id)
        user = find_by_id_user(user_id)
        if not user:
            raise NotFoundException("Not find user by ID")
        result = user_schema.dump(user)
        response = CustomResponse(data=result)
        return jsonify(response.to_dict()),200
    except SQLAlchemyError as sql:
        raise InternalServerException("Database error")
    except CustomAPIException as ex:
        raise ex
    except Exception as ex:
        raise InternalServerException("An unexpected error occurred")

# Create new jwt by refresh_token old
@api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@token_required
def refresh():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    try:
        # Attempt to create a new access token
        new_access_token = generate_accsse_token_by_refresh(current_user,role)
        response = CustomResponse(data =new_access_token)
        return jsonify(response.to_dict()), 200
    
    except Exception as e:
        return jsonify({'message': 'Access token expired, please provide a valid refresh token'}), 401