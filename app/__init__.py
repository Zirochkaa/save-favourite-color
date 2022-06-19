import os
from flask import Flask
from flask.cli import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create SQLAlchemy object, so we can use it later in our models.
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app_folder = os.path.dirname(os.path.realpath(__file__))
    load_dotenv(os.path.join(app_folder, ".env"))

    app.config.from_object("app.config.BaseConfig")

    db.init_app(app)

    Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(username: str):
        return User.query.filter_by(username=username).first()

    # blueprint for auth routes in our app
    from app.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
