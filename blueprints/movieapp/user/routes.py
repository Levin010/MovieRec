from flask import Blueprint, jsonify, request, url_for, render_template, flash, redirect
from .forms import SignupForm, LoginForm, ForgotPasswordForm, PasswordResetForm
from flask_jwt_extended import jwt_required
from flask_wtf.csrf import CSRFError
import jwt
import datetime
from flask_mail import Message
from ....extensions import mail, mongo
from ....config import Config
from passlib.hash import pbkdf2_sha256
from bson import ObjectId
from .models import User
from .forms import SignupForm, LoginForm

user_bp = Blueprint('user', __name__) 

@user_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()

    if request.method == "POST":
        if signup_form.validate_on_submit():
            return User().signup(signup_form)
        else:
            return jsonify({"errors": signup_form.errors}), 400  

    return render_template('user/signup.html', signup_form=signup_form) 

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if login_form.validate_on_submit():
            return User().login(login_form)
        else:
            return jsonify({"errors": login_form.errors}), 400  # Send validation errors as JSON

    return render_template('user/login.html', login_form=login_form)

@user_bp.route('/logout/', methods=['POST'])
@jwt_required()
def logout():
    try:
        csrf_token = request.headers.get("X-CSRF-TOKEN")
        

        if not csrf_token:
            return jsonify({"error": "CSRF token missing"}), 400

        return User().logout()

    except CSRFError as e:
        return jsonify({"error": "Invalid CSRF token", "message": str(e)}), 400



def send_reset_email(to_email, reset_link):
    msg = Message("Password Reset Request", sender="levdev1010@gmail.com", recipients=[to_email])
    msg.body = f"""
    Hi,

    You requested to reset your password. Click the link below to reset it:

    {reset_link}

    If you did not request this, please ignore this email.

    Regards,
    Movieapp Team
    """
    mail.send(msg)


@user_bp.route('/request-password-reset/', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'GET':
        form = ForgotPasswordForm()
        return render_template('user/request_password.html', form=form)

    # Handle both JSON and form-encoded data
    if request.content_type == "application/x-www-form-urlencoded":
        email = request.form.get("email")
    elif request.content_type == "application/json":
        data = request.get_json()
        email = data.get("email")
    else:
        return jsonify({"error": "Unsupported Content-Type"}), 415

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = mongo.db.users.find_one({"email": email})
    
    if user:
        token = jwt.encode(
            {"reset_password": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            Config.JWT_SECRET_KEY,
            algorithm="HS256"
        )
        reset_link = url_for('user.reset_password', token=token, _external=True)
        send_reset_email(user["email"], reset_link)

    return jsonify({"message": "If an account with this email exists, a reset link has been sent."})

@user_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Decode token to get user_id
        user_id = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])['reset_password']

        # Convert to ObjectId for MongoDB query
        user_id = ObjectId(user_id)
        user = mongo.db.users.find_one({"_id": user_id})

        if not user:
            flash("User not found!", "danger")
            return redirect(url_for('user.request_password_reset'))

    except Exception as e:
        flash("Invalid or expired token", "danger")
        return redirect(url_for('user.request_password_reset'))

    form = PasswordResetForm()
    
    if form.validate_on_submit():
        new_password = form.new_password.data
        
        if not new_password:
            flash("Password cannot be empty!", "danger")
            return render_template('user/reset_password.html', form=form)

        # Hash password and update DB
        updated_password = pbkdf2_sha256.hash(new_password)

        result = mongo.db.users.update_one({"_id": user_id}, {"$set": {"password": updated_password}})
        
        if result.modified_count == 0:
            flash("An error occurred. Try again.", "danger")
            return render_template('user/reset_password.html', form=form)

        flash("Your password has been updated!", "success")
        return redirect(url_for('main.index'))

    return render_template('user/reset_password.html', form=form)