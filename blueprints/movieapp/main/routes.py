from flask import Blueprint, render_template, session, redirect
from functools import wraps
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

main_bp = Blueprint('main', __name__) 

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@main_bp.route('/')
def index():
    return render_template('main/home.html')

@main_bp.route('/dashboard/')
@login_required
def dashboard():
    return render_template('main/dashboard.html')