import os

from flask import Flask
from flask.cli import load_dotenv
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object, so we can use it later in our models.
db = SQLAlchemy()


def create_app(config: str = "app.config.ProdConfig") -> Flask:
    app = Flask(__name__)

    app_folder = os.path.dirname(os.path.realpath(__file__))
    load_dotenv(os.path.join(app_folder, ".env"))

    app.config.from_object(config)

    db.init_app(app)

    Migrate(app, db)

    toolbar = DebugToolbarExtension()
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config["DEBUG_TB_PANELS"] = (
        "flask_debugtoolbar.panels.versions.VersionDebugPanel",
        "flask_debugtoolbar.panels.timer.TimerDebugPanel",
        "flask_debugtoolbar.panels.headers.HeaderDebugPanel",
        "flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel",
        "flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel",
        "flask_debugtoolbar.panels.template.TemplateDebugPanel",
        "app.debugtoolbar.sqlalchemy_panel.SQLAlchemyDebugPanel",
        "flask_debugtoolbar.panels.logger.LoggingPanel",
        "flask_debugtoolbar.panels.route_list.RouteListDebugPanel",
        "flask_debugtoolbar.panels.profiler.ProfilerDebugPanel",
        "flask_debugtoolbar.panels.g.GDebugPanel",
    )
    toolbar.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: int):
        return db.session.get(User, user_id)

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
