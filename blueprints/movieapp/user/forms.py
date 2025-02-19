from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from werkzeug.security import check_password_hash
from bson import ObjectId

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=30, message="Username must be between 3 and 30 characters"),
        Regexp(r'^[\w]+$', message="Username can only contain letters, numbers, and underscores")
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address"),
        Length(max=120, message="Email must be less than 120 characters")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]',
               message="Password must contain at least one letter, one number, and one special character")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    def validate_email(self, email):
        from extensions import db  #to avoid circular imports
        if mongo.db.users.find_one({"email": email.data}):
            raise ValidationError('Email address is already registered')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    
    def validate_credentials(self):
        from extensions import db  
        from passlib.hash import pbkdf2_sha256
        
        user = mongo.db.users.find_one({"email": self.email.data})
        if not user or not pbkdf2_sha256.verify(self.password.data, user['password']):
            raise ValidationError('Invalid email or password')
        return user
