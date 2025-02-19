from flask import Flask, render_template
from blueprints.movieapp.user.routes import user_bp
from blueprints.movieapp.main.routes import main_bp
from extensions import db



app = Flask(__name__, template_folder='templates',  static_folder='static')
app.secret_key = b'\x8fn~\xe9\x83\xe0\xdb\x9eJ?j&Y\xf1\x9a\xfe'

app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')


if __name__ == '__main__':
    app.run(debug=True) 