from flask import Flask
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from .extensions import mongo, init_db, mail
import os
from .config import Config
from .blueprints.movieapp.user.routes import user_bp
from .blueprints.movieapp.main.routes import main_bp


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

if not os.getenv("MONGO_URI"):
    raise ValueError("MONGO_URI is not set in the environment variables")


# Initialize extensions
init_db(app)
mail.init_app(app)

jwt = JWTManager(app)
csrf = CSRFProtect(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
