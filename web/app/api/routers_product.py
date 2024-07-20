from flask import Blueprint, jsonify, request
from ..service.product_service import create_product
from ..utils.response import CustomResponse
from ..auth import token_required, role_required

product = Blueprint('product', __name__)


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
    except Exception as ex:
        raise ex