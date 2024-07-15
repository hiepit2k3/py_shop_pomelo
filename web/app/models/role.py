from ..db import db
from sqlalchemy import Column, Integer, String

class Role(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
