from flask import request
from app.models.product import Product
from ..db import db
from sqlalchemy.exc import SQLAlchemyError



def create_product(data):
    try:
        
        result = create_product_with_sql(data)
        return result
    except SQLAlchemyError as sql:
        print("loi sql")
        raise sql
    except Exception as ex:
        print("loi khac")
        raise ex

def create_product_with_sql(data):
    try:
        product = Product(
            name = data['name'],
            price = data['price'],
            quantity = data['quantity'],
            image = data['image']
        )
        db.session.add(product)
        db.session.commit()
        return product
    except SQLAlchemyError as sql:
        print("loi sql nua")
        raise sql
    
def find_by_id_product(id):
    try:
        product  = Product.query.filter(Product.id == id).first()
        return product
    except SQLAlchemyError as sql:
        raise sql