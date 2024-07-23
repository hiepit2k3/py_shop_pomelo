from flask_cors import CORS
from flask import Flask, jsonify
from .db import db  # Import SQLAlchemy instance từ db.py
from .api.routers_user import api  # Import blueprint từ routers_user.py
from .api.routers_product import product
from exceptions import CustomAPIException
from .utils.response import CustomResponse
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://default:AR9SrBhEsPg3@ep-orange-term-a4m8nc1a.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
    
    jwt = JWTManager(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(product, url_prefix='/api')
    
    @app.errorhandler(CustomAPIException)
    def handle_custom_error(error):
        status_code = error.status_code if hasattr(error, 'status_code') else 500
        errors = {
            'error': error.message,
        }
        response = CustomResponse(data=errors, status_code=status_code)
        return jsonify(response.to_dict()), status_code
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
