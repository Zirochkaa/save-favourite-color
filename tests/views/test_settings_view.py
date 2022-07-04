from typing import Optional

import pytest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests.helpers import check_menu


def test_settings_view(test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends GET request to `/settings` page
    THEN `/settings` page should be shown
    """
    response = test_login_client.get("/settings")

    assert response.status_code == 200
    check_menu(response=response, current_user=current_user)
    assert "Please pick up a new color" in response.text


def test_settings_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/settings` page
    THEN redirect to `/login` page should occur
    """
    response = test_client.get("/settings")

    assert response.status_code == 302
    assert "Redirecting..." in response.text
    assert "/login" in response.headers.get("Location", "")


def test_settings_view_post(test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends POST request to `/settings` page with correct `color` in request form
    THEN `User.favourite_color` should be updated with new `color` and `/profile` page should be shown
    """
    color = "purple"
    response = test_login_client.post("/settings", data={"color": color})

    assert response.status_code == 200
    assert current_user.favourite_color == color
    check_menu(response=response, current_user=current_user)
    assert f"Your favourite color is {color}" in response.text


@pytest.mark.parametrize(
    "data,error_text",
    (
        (None, "We do not support such (None) color yet"),
        ({}, "We do not support such (None) color yet"),
        ({"color": None}, "We do not support such (None) color yet"),
        ({"color": "gold"}, "We do not support such (gold) color yet"),
    )
)
def test_settings_view_post_incorrect_color(data: dict, error_text: str, test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends POST request to `/settings` page with incorrect `color` (empty, wrong value, etc) in request form
    THEN `/settings` page should be shown with `We do not support such ({color}) color yet` text
    """
    response = test_login_client.post("/settings", data=data)

    assert response.status_code == 200
    assert "Please pick up a new color" in response.text
    assert error_text in response.text


@pytest.mark.parametrize(
    "data",
    (
        None,   # Incorrect data
        {},   # Incorrect data
        {"color": None},   # Incorrect data
        {"color": "gold"},   # Incorrect data
        {"color": "blue"},   # Correct data
    )
)
def test_settings_view_anonymous_user_post(data: Optional[dict], test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends POST request to `/settings` page with both correct `color` and with
        incorrect `color` (empty, wrong value, etc) in request form
    THEN redirect to `/login` page should occur
    """
    response = test_client.post("/settings", data=data)

    assert response.status_code == 302
    assert "Redirecting..." in response.text
    assert "/login" in response.headers.get("Location", "")
