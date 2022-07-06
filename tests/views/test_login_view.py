from typing import Optional

import pytest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user, UserMixin
from werkzeug.security import check_password_hash

from app import db
from app.models import User
from tests.helpers import check_menu


def test_login_view(test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends GET request to `/login` url
    THEN redirect to `/profile` page should occur
    """
    response = test_login_client.get("/login")

    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response.text
    assert "/profile" == response.headers.get("Location", "")


def test_login_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/login` url
    THEN `/login` page should be shown
    """
    response = test_client.get("/login")

    assert response.status_code == 200
    check_menu(response=response, current_user=current_user)
    assert '<h3 class="mb-3 color-text">Please sign in</h3>' in response.text
    assert '<button class="w-100 btn btn-lg" style="color:#337def;background-color:#fcc729" ' \
           'type="submit">Sign in</button>' in response.text


@pytest.mark.parametrize(
    "data",
    (
        None,  # Incorrect data
        {},  # Incorrect data
        {"username": "", "password": ""},  # Incorrect data
        {"username": "Thor", "password": "Thor"},  # Correct data
    )
)
def test_login_view_post(data: Optional[dict], test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends POST request to `/login` url with both:
        - correct `username` and `password` in request form;
        - with incorrect data in request form;
    THEN redirect to `/profile` page should occur
    """

    response = test_login_client.post("/login", data=data)

    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response.text
    assert "/profile" == response.headers.get("Location", "")


def test_login_view_post_anonymous_user_correct_data(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/login` url with correct `username` and `password` in request form
    THEN AnonymousUser should be logged in and redirect to `/profile` page should occur
    """
    # Here we don't check if `current_user` object is an instance of `AnonymousUserMixin` class
    # because before sending a request there is no `current_user`, so `current_user` is `None`.
    assert not current_user

    username = "Gordon"
    password = "Ramsay"

    response = test_client.post("/login", data={"username": username, "password": password})

    user = User.query.filter_by(username=username).first()
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response.text
    assert "/profile" == response.headers.get("Location", "")
    assert current_user and isinstance(current_user, UserMixin)
    assert current_user.username == user.username
    assert current_user.favourite_color == user.favourite_color
    assert check_password_hash(current_user.password, password)


@pytest.mark.parametrize(
    "data,error_text",
    (
        (None, "Username/password can not be empty"),
        ({}, "Username/password can not be empty"),
        ({"username": "", "password": "     "}, "Username/password can not be empty"),
        ({"username": "     ", "password": ""}, "Username/password can not be empty"),
        ({"username": "Thor_wrong", "password": "Thor"}, "User with such username/password does not exist"),
        ({"username": "Thor", "password": "Thor_wrong"}, "User with such username/password does not exist"),
    )
)
def test_login_view_post_anonymous_user_incorrect_data(data: Optional[dict], error_text: str, test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/login` page with incorrect `username` and/or `password`
        (empty, wrong value, etc) in request form
    THEN `/login` page should be shown with appropriate error text and `400` status code
    """
    # Here we don't check if `current_user` object is an instance of `AnonymousUserMixin` class
    # because before sending a request there is no `current_user`, so `current_user` is `None`.
    assert not current_user

    response = test_client.post("/login", data=data)

    assert response.status_code == 400
    check_menu(response=response, current_user=current_user)
    assert error_text in response.text


def test_login_view_post_anonymous_user_not_active(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/login` page with `username` and `password` for not active User
    THEN `/login` page should be shown with `Something went wrong during login process` text and `400` status code
    """
    # Here we don't check if `current_user` object is an instance of `AnonymousUserMixin` class
    # because before sending a request there is no `current_user`, so `current_user` is `None`.
    assert not current_user

    username = "Gordon"
    password = "Ramsay"
    # By default, each test user has `is_active=True`. For this test we have to manually switch `is_active` to `False.
    user = User.query.filter_by(username=username).first()
    assert user.is_active is True
    user.is_active = False
    db.session.add(user)
    db.session.commit()

    user = User.query.get(user.id)
    assert user.is_active is False

    response = test_client.post("/login", data={"username": user.username, "password": password})

    assert response.status_code == 400
    check_menu(response=response, current_user=current_user)
    assert "Something went wrong during login process" in response.text
