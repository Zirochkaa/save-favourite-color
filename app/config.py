import os


class BaseConfig:
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    TESTING = os.getenv("TESTING", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
