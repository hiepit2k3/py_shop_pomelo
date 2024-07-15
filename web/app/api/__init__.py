# backend/app/__init__.py
from flask_cors import CORS
from flask import Flask,jsonify
from ..db import db  # Import SQLAlchemy instance từ db.py
from .routers import api  # Import blueprint từ routes.py
from exceptions import CustomAPIException
from ..utils.response import CustomResponse

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/db_shop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config.from_object(config)  # Cấu hình ứng dụng từ config.py

    db.init_app(app)  # Khởi tạo SQLAlchemy với ứng dụng Flask
    with app.app_context():
        db.create_all()  # Tạo tất cả các bảng nếu chưa tồn tại

    # Đăng ký blueprint từ routes.py
    app.register_blueprint(api, url_prefix='/api')
    
    # Đăng ký hàm xử lý lỗi
    @app.errorhandler(CustomAPIException)
    def handle_custom_error(error):
        status_code = error.status_code if hasattr(error, 'status_code') else 500
        errors = {
            'error': error.message,
        }
        response = CustomResponse(data=errors,error_code = status_code)
        return jsonify(response.to_dict()), status_code
    
     # Cấu hình CORS cho ứng dụng Flask
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
