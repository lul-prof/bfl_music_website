from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register the format_datetime filter
    @app.template_filter('format_datetime')
    def format_datetime(value):
        if value is None:
            return ""
        return value.strftime('%B %d, %Y %H:%M')

    @app.template_filter('format_currency')
    def format_currency(value):
        return "Ksh {:,.2f}".format(value)

    from app.routes import auth, main, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    return app