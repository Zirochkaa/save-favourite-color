import os
from flask import Flask
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app_folder = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(app_folder, ".env"))

app = Flask(__name__)
app.config.from_object("app.config.BaseConfig")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
