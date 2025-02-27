from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_mail import Mail
import os

load_dotenv()  

mongo = PyMongo()
mail = Mail()

def init_db(app):
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set or is empty!")

    
    app.config["MONGO_URI"] = mongo_uri

    

    try:
        mongo.init_app(app)

        # assigns the database
        mongo.db = mongo.cx["levdev"]  

        

    except Exception as e:
        print("❌ Flask-PyMongo Initialization Failed:", str(e))
