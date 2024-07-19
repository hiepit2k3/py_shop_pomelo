from ..db import db
import pytz
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    quantity = Column(Integer,nullable=False)
    image = Column(String, nullable=False)
    
    def __repr__(self):
        return f'<Product {self.name}>'