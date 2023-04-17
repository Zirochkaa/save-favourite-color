from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient

from tests import helpers


@pytest.mark.parametrize(
    "client",
    (
        "test_client",
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_logout_view(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends GET request to `/auth/logout` url
    THEN User should be logged out and redirect to `/` page should occur
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get(helpers.logout_endpoint)

    assert response.status_code == 302
    assert helpers.redirect_h_tag in response.text
    assert helpers.home_endpoint == response.headers.get("Location", "")


@pytest.mark.parametrize(
    "client",
    (
        "test_client",
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_logout_view_post(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends POST request to `/auth/logout` url
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post(helpers.logout_endpoint)

    assert response.status_code == 405
    assert helpers.method_not_allowed_h_tag in response.text
