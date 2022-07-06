from typing import Optional

import pytest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user, UserMixin
from werkzeug.security import check_password_hash

from app.models import Color, User
from tests.helpers import check_menu


def test_signup_view(test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends GET request to `/signup` url
    THEN redirect to `/profile` page should occur
    """
    response = test_login_client.get("/signup")

    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response.text
    assert "/profile" == response.headers.get("Location", "")


def test_signup_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/signup` url
    THEN `/signup` page should be shown
    """
    response = test_client.get("/signup")

    assert response.status_code == 200
    check_menu(response=response, current_user=current_user)
    assert '<h3 class="mb-3 color-text">Please sign up</h3>' in response.text
    assert '<button class="w-100 btn btn-lg" style="color:#337def;background-color:#fcc729" ' \
           'type="submit">Sign up</button>' in response.text


@pytest.mark.parametrize(
    "data",
    (
        None,  # Incorrect data
        {},  # Incorrect data
        {"username": "", "password": "", "color": ""},  # Incorrect data
        {"username": "Thor", "password": "Thor", "color": "blue"},  # Correct data
    )
)
def test_signup_view_post(data: Optional[dict], test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends POST request to `/signup` url with both:
        - correct `username`, `password` and `color` in request form;
        - with incorrect data in request form;
    THEN redirect to `/profile` page should occur
    """

    response = test_login_client.post("/signup", data=data)

    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response.text
    assert "/profile" == response.headers.get("Location", "")


def test_signup_view_post_anonymous_user_correct_data(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/signup` url with correct `username`, `password` and `color`
        in request form
    THEN a new User should be created and `/signup` page should be shown with content of `after_signup` template
    """
    username = "qwerty"
    password = "qwerty123"
    color = Color.get_random_color()
    response = test_client.post("/signup", data={"username": username, "password": password, "color": color.color})

    assert response.status_code == 200
    assert '<h3 class="color-text">You successfully signed up.</h3>' in response.text
    assert '<h3 class="color-text">Now you can proceed to login page. The link to login page is located in the ' \
           'upper right corner.</h3>' in response.text

    created_user = User.query.filter_by(username=username).first()
    assert created_user
    assert created_user and isinstance(created_user, UserMixin)
    assert created_user.username == username
    assert created_user.favourite_color == color.color
    assert check_password_hash(created_user.password, password)


@pytest.mark.parametrize(
    "data,error_text",
    (
        (None, "Username/password can not be empty"),
        ({}, "Username/password can not be empty"),
        ({"username": "", "password": "     ", "color": "blue"}, "Username/password can not be empty"),
        ({"username": "     ", "password": "", "color": "blue"}, "Username/password can not be empty"),
        ({"username": "Thor", "password": "Thor", "color": "blue"}, "User with such username already exist"),
        ({"username": "Thor_new", "password": "Thor", "color": ""}, "We do not support such () color yet"),
        ({"username": "Thor_new", "password": "Thor", "color": None}, "We do not support such (None) color yet"),
        ({"username": "Thor_new", "password": "Thor", "color": "gold"}, "We do not support such (gold) color yet"),
        ({"username": "Thor_new", "password": "Thor"}, "We do not support such (None) color yet"),
    )
)
def test_signup_view_post_anonymous_user_incorrect_data(data: Optional[dict], error_text: str,
                                                        test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/signup` page with incorrect `username` and/or `password`
        and/or color (empty, wrong value, etc) in request form
    THEN `/signup` page should be shown with appropriate error text and `400` status code
    """
    response = test_client.post("/signup", data=data)

    assert response.status_code == 400
    check_menu(response=response, current_user=current_user)
    assert error_text in response.text
