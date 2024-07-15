from app.models.token import Token
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

def create_token_with_sql(data_user,access_token,refresh_token):
    try:
        token = Token(
            refresh_token = refresh_token,
            access_token = access_token,
            user_id = data_user.id,
        )
        db.session.add(token)
        db.session.commit()
        return token
    except SQLAlchemyError as sql:
        raise sql