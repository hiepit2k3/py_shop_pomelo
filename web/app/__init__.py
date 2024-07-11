from flask import Flask
from .routers import api_blueprint  # Import blueprint từ routes.py

def create_app():
    app = Flask(__name__,static_folder="../static")
    app.config.from_object('config')  # Cấu hình ứng dụng từ config.py

    # Đăng ký blueprint từ routes.py
    app.register_blueprint(api_blueprint)

    return app
