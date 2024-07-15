from ..db import db
import pytz
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class User(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    date_create = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    role_id = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
