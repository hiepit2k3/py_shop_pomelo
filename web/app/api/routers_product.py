from flask import Blueprint, jsonify, request
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ..models.schema.product_schema import ProductSchema
from ..service.product_service import create_product, find_by_id_product
from ..utils.response import CustomResponse
from ..auth import token_required, role_required
from exceptions import NotFoundException,InvalidCredentialsException,ConflictException,ForbiddenException

product = Blueprint('product', __name__)
product_schema = ProductSchema()

@product.route('/product', methods=['GET'])
def get_product():
    return "this product"


@product.route('product/create', methods=['POST'])
@role_required('admin')
@token_required
def create_products():
    try:
        data  = request.get_json()
        result_data = create_product(data)
        if not result_data:
                raise ValueError("No input data provided")
        response = CustomResponse(data={'message': 'add product succesfully!'})
        return jsonify(response.to_dict()), 201
    except SQLAlchemyError as sql:
        raise sql
    except Exception as ex:
        raise ex
    
@product.route('product/find/<int:id>', methods=['GET'])
def find_by_id_products(id):
    try:
        result = find_by_id_product(id)
        if not result:
            raise NotFoundException("Not find user by ID")
        result_data = product_schema.dump(result)
        response = CustomResponse(data=result_data)
        return jsonify(response.to_dict()), 200
    except SQLAlchemyError as sql:
        raise sql