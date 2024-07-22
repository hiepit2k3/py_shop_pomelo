# backend/app/__init__.py
from flask_cors import CORS
from flask import Flask,jsonify
from ..db import db  # Import SQLAlchemy instance từ db.py
from .routers_user import api  # Import blueprint từ routes.py
from .routers_product import product
from exceptions import CustomAPIException
from ..utils.response import CustomResponse
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/db_shop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_asQdsw9c'  # Flask cũng cần khóa bí mật cho một số tính năng khác
    app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'  # Đặt JWT_SECRET_KEY là bắt buộc
    
    jwt = JWTManager(app)

    db.init_app(app)  # Khởi tạo SQLAlchemy với ứng dụng Flask
    with app.app_context():
        db.create_all()  # Tạo tất cả các bảng nếu chưa tồn tại

    # Đăng ký blueprint từ routes.py
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(product, url_prefix='/api')
    
    # Đăng ký hàm xử lý lỗi
    @app.errorhandler(CustomAPIException)
    def handle_custom_error(error):
        status_code = error.status_code if hasattr(error, 'status_code') else 500
        errors = {
            'error': error.message,
        }
        response = CustomResponse(data=errors,status_code = status_code)
        return jsonify(response.to_dict()), status_code
    
     # Cấu hình CORS cho ứng dụng Flask
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
