from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user, UserMixin
from werkzeug.security import check_password_hash

from app import db
from app.models import User
from tests import helpers
from tests.helpers import check_menu


@pytest.mark.parametrize(
    "client",
    (
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_login_view(client: str, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends GET request to `/auth/login` url
    THEN redirect to `/profile/` page should occur
    """
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.get(helpers.login_endpoint)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.profile_endpoint == response.headers.get("Location", "")


def test_login_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/auth/login` url
    THEN `/auth/login` page should be shown
    """
    response = test_client.get(helpers.login_endpoint)

    assert response.status_code == 200
    check_menu(response=response, current_user=current_user)
    assert '<h3 class="mb-3 color-text">Please sign in</h3>' in response.text
    assert '<button class="w-100 btn btn-lg general-button" type="submit">Sign in</button>' in response.text


@pytest.mark.parametrize(
    "data",
    (
        None,  # Incorrect data
        {},  # Incorrect data
        {"username": "", "password": ""},  # Incorrect data
        {"username": "Thor", "password": "Thor"},  # Correct data
    )
)
@pytest.mark.parametrize(
    "client",
    (
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_login_view_post(data: Optional[dict], client: str, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends POST request to `/auth/login` url with both:
        - correct `username` and `password` in request form;
        - with incorrect data in request form;
    THEN redirect to `/profile/` page should occur
    """
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.post(helpers.login_endpoint, data=data)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.profile_endpoint == response.headers.get("Location", "")


def test_login_view_post_anonymous_user_correct_data(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/auth/login` url with correct `username` and `password` in request form
    THEN AnonymousUser should be logged in and redirect to `/profile/` page should occur
    """
    # Here we don't check if `current_user` object is an instance of `AnonymousUserMixin` class
    # because before sending a request there is no `current_user`, so `current_user` is `None`.
    assert not current_user

    username = "Gordon"
    password = "Ramsay"

    response = test_client.post(helpers.login_endpoint, data={"username": username, "password": password})

    user = User.query.filter_by(username=username).first()
    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.profile_endpoint == response.headers.get("Location", "")
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
    WHEN an AnonymousUser sends POST request to `/auth/login` page with incorrect `username` and/or `password`
        (empty, wrong value, etc) in request form
    THEN `/auth/login` page should be shown with appropriate error text and `400` status code
    """
    # Here we don't check if `current_user` object is an instance of `AnonymousUserMixin` class
    # because before sending a request there is no `current_user`, so `current_user` is `None`.
    assert not current_user

    response = test_client.post(helpers.login_endpoint, data=data)

    assert response.status_code == 400
    check_menu(response=response, current_user=current_user)
    assert error_text in response.text


def test_login_view_post_anonymous_user_not_active(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/auth/login` page with `username` and `password` for not active User
    THEN `/auth/login` page should be shown with `Something went wrong during login process` text and `400` status code
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

    response = test_client.post(helpers.login_endpoint, data={"username": user.username, "password": password})

    assert response.status_code == 400
    check_menu(response=response, current_user=current_user)
    assert "Something went wrong during login process" in response.text


def test_login_view_post_anonymous_user_next_parameter(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/auth/login` url with `next` url parameter and correct data in
        request form;
    THEN redirect to `next` url page should occur
    """
    referer = f'http://localhost:5000{helpers.login_endpoint}?next={helpers.settings_endpoint}'
    response = test_client.post(helpers.login_endpoint, data={"username": "Thor", "password": "Thor"},
                                headers={'Referer': referer})

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.settings_endpoint == response.headers.get("Location", "")
