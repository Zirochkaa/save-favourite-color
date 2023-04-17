import os
from flask import Flask
from flask.cli import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create SQLAlchemy object, so we can use it later in our models.
db = SQLAlchemy()


def create_app(config: str = "app.config.BaseConfig") -> Flask:
    app = Flask(__name__)

    app_folder = os.path.dirname(os.path.realpath(__file__))
    load_dotenv(os.path.join(app_folder, ".env"))

    app.config.from_object(config)

    db.init_app(app)

    Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(user_id)

    # blueprint for auth parts of our app
    from app.auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    # blueprint for admin panel parts of our app
    from app.admin.admin import admin_bp
    app.register_blueprint(admin_bp)

    # blueprint for profile parts of our app
    from app.profile.profile import profile_bp
    app.register_blueprint(profile_bp)

    # blueprint for general parts of our app
    from app.general.general import general_bp
    app.register_blueprint(general_bp)

    return app
