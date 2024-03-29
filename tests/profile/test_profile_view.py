from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests import helpers


@pytest.mark.parametrize(
    "client,is_admin",
    (
        ("test_client_with_logged_in_user", False),
        ("test_client_with_logged_in_admin", True),
    )
)
def test_profile_view(client: str, is_admin: bool, request: FixtureRequest):
    """
    GIVEN a (User, Admin User)
    WHEN a (User, Admin User) sends GET request to `/profile/` page
    THEN `/profile/` page should be shown
    """
    client: FlaskLoginClient = request.getfixturevalue(client)
    response = client.get(helpers.profile_endpoint)

    assert current_user.is_admin is is_admin
    assert response.status_code == 200
    helpers.check_menu(response=response, current_user=current_user)
    assert f"Your favourite color is {current_user.favourite_color}." in response.text


def test_profile_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/profile/` page
    THEN redirect to `/auth/login` page should occur
    """
    response = test_client.get(helpers.profile_endpoint)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.login_endpoint in response.headers.get("Location", "")


@pytest.mark.parametrize(
    "client",
    (
        "test_client",
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin"
    )
)
def test_profile_view_post(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends POST request to `/profile/` page
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post(helpers.profile_endpoint)

    assert response.status_code == 405
    assert helpers.method_not_allowed_h_tag in response.text
