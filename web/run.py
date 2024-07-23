import sys
import os

# Thêm thư mục web vào đường dẫn tìm kiếm mô-đun
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Vercel yêu cầu chạy trên cổng 8000
