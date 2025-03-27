import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # Set to True in production (HTTPS only)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN"
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_CSRF_METHODS = ["POST", "PUT", "DELETE"]
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET')  # CSRF protection
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_HEADERS = ["X-CSRF-TOKEN"]
    WTF_CSRF_COOKIE_NAME = "csrf_access_token"

    # Flask Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587)) 
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"  
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


    #TMDB API
    API_KEY = os.getenv("API_KEY")
