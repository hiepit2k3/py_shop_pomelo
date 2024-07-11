from flask import Blueprint, jsonify, render_template
from .models import User  # Import các model từ models.py

api_blueprint = Blueprint('main', __name__,template_folder='../templates')

@api_blueprint.route('/home')
def get_users():
    return show_index_page()

def show():
    return show_index_page()

def show_index_page(**params):
    return render_template("index.html",**params)