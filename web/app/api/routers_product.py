from flask import Blueprint, jsonify, request


product = Blueprint('product', __name__)

@product.route('/product', methods=['GET'])
def get_product():
    return "this product"