import os


class BaseConfig:
    DEBUG = os.getenv("FLASK_DEBUG", 'false').lower() == 'true'
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    TESTING = os.getenv("TESTING", 'false').lower() == 'true'
    SQLALCHEMY_RECORD_QUERIES = os.getenv("SQLALCHEMY_RECORD_QUERIES", 'false').lower() == 'true'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", 'false').lower() == 'true'


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
