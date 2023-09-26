from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('demo_password')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://juanasoto:{os.getenv('demo_password')}@localhost:3306/user_login_sys"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

google_blueprint = make_google_blueprint(client_id=os.getenv('client_id'), 
client_secret=os.getenv('client_secret'), scope=['email', 'profile'], 
offline=True)

app.register_blueprint(google_blueprint, url_prefix='/google_login')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
