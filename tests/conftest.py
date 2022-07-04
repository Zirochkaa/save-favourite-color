import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient
from flask_migrate import upgrade
from app import create_app, db
from app.models import User


@pytest.fixture(scope="function")
def app_empty_db() -> Flask:
    """
    Get application.
    """
    app = create_app(config="app.config.TestConfig")

    with app.app_context():
        db.engine.execute("DROP TABLE IF EXISTS alembic_version")
        db.session.remove()
        db.drop_all()

        yield app

        db.engine.execute("DROP TABLE IF EXISTS alembic_version")
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def app_with_migrations(app_empty_db) -> Flask:
    """
    Get application with applied migrations.
    """
    upgrade()
    return app_empty_db


@pytest.fixture(scope="function")
def test_client(app_with_migrations) -> FlaskClient:
    """
    Get test client.
    """
    with app_with_migrations.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def test_login_client(app_with_migrations) -> FlaskLoginClient:
    """
    Get test client with logged in user.
    """
    app_with_migrations.test_client_class = FlaskLoginClient
    user = User.get_random_user()

    with app_with_migrations.test_client(user=user) as client:
        yield client


@pytest.fixture(scope="function")
def test_user_object() -> User:
    """
    Get `User` class instance.
    """
    return User(username="Spiderman", password="Peter", favourite_color="green")


@pytest.fixture(scope="function")
def test_user(app_with_migrations) -> User:
    """
    Get `User` class instance from db.
    """
    return User.get_random_user()
