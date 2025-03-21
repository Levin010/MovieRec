from flask import Blueprint, render_template, session, redirect
from flask_jwt_extended import jwt_required
from ..user.forms import SignupForm, LoginForm
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

main_bp = Blueprint('main', __name__) 


@main_bp.route('/')
def index():

    return render_template('main/index.html')


@main_bp.route('/dashboard/')
@jwt_required()
def dashboard():
    return render_template('main/dashboard.html')