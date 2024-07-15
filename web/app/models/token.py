from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from datetime import datetime
import pytz
from ..db import db

class Token(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String, unique=True, index=True, nullable=False)
    access_token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
