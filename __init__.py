# Dev Dominic Minnich 2024
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    csrf = CSRFProtect(app)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models import User, Device
        db.create_all()

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
