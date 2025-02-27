from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from passlib.hash import pbkdf2_sha256
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
    
    password = PasswordField('Password', render_kw={"id": "signup-password"}, validators=[
        DataRequired(message="Password is required"),
        Length(min=8, max=64, message="Password must be at least 8 characters long"),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character")
    ])
    
    confirm_password = PasswordField('Confirm Password', render_kw={"id": "signup-confirm-password"}, validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    def validate_email(self, email):
        from MovieApp.extensions import mongo
        try:
            users_collection = mongo.db.users
            if users_collection.find_one({"email": email.data}):
                raise ValidationError('Email address is already registered')
        except Exception as e:
            raise ValidationError(f"Database connection failed: {str(e)}")

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    
    password = PasswordField('Password', render_kw={"id": "login-password"}, validators=[
        DataRequired(message="Password is required")
    ])
    
    def validate_credentials(self):
        from MovieApp.extensions import mongo
        try:
            users_collection = mongo.db.users
            user = users_collection.find_one({"email": self.email.data})
            if not user or not pbkdf2_sha256.verify(self.password.data, user['password']):
                raise ValidationError('Invalid email or password')
            return user
        except Exception as e:
            raise ValidationError(f"Database connection failed: {str(e)}")
        
class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class PasswordResetForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Reset Password")
