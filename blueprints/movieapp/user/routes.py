from flask import Flask,Blueprint, render_template, request, redirect, url_for
from .models import User


user_bp = Blueprint('user', __name__) 



@user_bp.route('/signup/', methods=['POST'])
def signup():
    return User().signup()

@user_bp.route('/signout/')
def signout():
    return User().signout()

@user_bp.route('/login/', methods=['POST'])
def login():
    return User().login()

