from ..db import db
import pytz
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(float, nullable=False)
    quantity = Column(Integer,nullable=False)
    images = relationship('ProductImage', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    def __repr__(self):
        return f'<ProductImage {self.url}>'