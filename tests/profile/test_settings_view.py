from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests import helpers


@pytest.mark.parametrize(
    "client",
    (
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_settings_view(client: str, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends GET request to `/profile/settings/color` page
    THEN `/profile/settings/color` page should be shown
    """
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.get(helpers.settings_endpoint)

    assert response.status_code == 200
    helpers.check_menu(response=response, current_user=current_user)
    assert "Please pick up a new color" in response.text


def test_settings_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/profile/settings/color` page
    THEN redirect to `/auth/login` page should occur
    """
    response = test_client.get(helpers.settings_endpoint)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.login_endpoint in response.headers.get("Location", "")


@pytest.mark.parametrize(
    "client",
    (
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_settings_view_post(client: str, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends POST request to `/profile/settings/color` page with correct `color` in request form
    THEN `User.favourite_color` should be updated with new `color` and redirect to `/profile/` page should occur
    """
    color = "purple"
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.post(helpers.settings_endpoint, data={"color": color})

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.profile_endpoint in response.headers.get("Location", "")


@pytest.mark.parametrize(
    "data,error_text",
    (
        (None, "We do not support such (None) color yet"),
        ({}, "We do not support such (None) color yet"),
        ({"color": None}, "We do not support such (None) color yet"),
        ({"color": "gold"}, "We do not support such (gold) color yet"),
    )
)
@pytest.mark.parametrize(
    "client",
    (
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_settings_view_post_incorrect_color(data: dict, error_text: str, client: str, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends POST request to `/profile/settings/color` page with incorrect `color`
        (empty, wrong value, etc) in request form
    THEN `/profile/settings/color` page should be shown with `We do not support such ({color}) color yet` text
    """
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.post(helpers.settings_endpoint, data=data)

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
    WHEN an AnonymousUser sends POST request to `/profile/settings/color` page with both correct `color` and with
        incorrect `color` (empty, wrong value, etc) in request form
    THEN redirect to `/auth/login` page should occur
    """
    response = test_client.post(helpers.settings_endpoint, data=data)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.login_endpoint in response.headers.get("Location", "")
