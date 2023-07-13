import os


class BaseConfig:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", False)
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    TESTING = os.getenv("TESTING", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL_TEST"]
