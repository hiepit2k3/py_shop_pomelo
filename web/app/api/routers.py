from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.role import Role
from ..models.schema.user_schema import UserSchema
from ..models.schema.token_schama import Tokenschema
from app.service.user_service import create_user, get_user_by_username_and_pass,find_by_id_user
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from exceptions import BadRequestException, ConflictException, InternalServerException, InvalidCredentialsException, NotFoundException
from ..service.role_service import create_with_sql
from ..utils.response import CustomResponse
from exceptions import CustomAPIException
from ..auth import token_required


api = Blueprint('main', __name__)
user_schema = UserSchema()
token_schema = Tokenschema()


# 
@api.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        data_save = create_user(data)
        if not data:
            raise ValueError("No input data provided")
        print("data cuoi cung",data_save)
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
        raise InternalServerException("An unexpected error occurred")
    
@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        result = get_user_by_username_and_pass(data['username'],data['password'])
        if not result:
            raise InvalidCredentialsException("Username or password incorect, Please input again!")
        respone = CustomResponse(data=result)
        return jsonify(respone.to_dict()), 200
    
    except IntegrityError as ie:
        raise ConflictException("Username already exists")

    except ValueError as ve:
        raise BadRequestException(str(ve))

    except SQLAlchemyError as se:
        raise InternalServerException("Database error")
    
    except Exception as ex:
        raise ex

    
@api.route('/role/register', methods=['POST'])
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
    
@api.route('/user/find/<int:user_id>', methods=['GET'])
@token_required
def find_by_id_user_route(user_id):
    try:
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