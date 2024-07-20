from app.models.role import Role
from ..db import db
from sqlalchemy.exc import SQLAlchemyError

def create_with_sql(data):
    try:
        new_data = Role(
            name = data['name'],
            description =['description']
        )
        db.session.add(new_data)
        db.session.commit()
        return new_data
    except SQLAlchemyError as sql:
        print('sdjhfjks:',sql)
        raise sql
    