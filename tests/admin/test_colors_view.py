from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests import helpers


def test_admin_colors_view_regular_user(test_client_with_logged_in_user: FlaskLoginClient):
    """
    GIVEN an User
    WHEN an User sends GET request to `/admin/colors` page
    THEN `404` error code should be returned along with template for 404 page
    """
    response = test_client_with_logged_in_user.get(helpers.admin_colors_endpoint)

    assert response.status_code == 404
    helpers.check_menu(response=response, current_user=current_user)
    assert helpers.page_not_found_h_tag in response.text


def test_admin_colors_view_admin_user(test_client_with_logged_in_admin: FlaskLoginClient):
    """
    GIVEN a Admin User
    WHEN a Admin User sends GET request to `/admin/colors` page
    THEN `/admin/colors` page should be shown
    """
    response = test_client_with_logged_in_admin.get(helpers.admin_colors_endpoint)

    assert current_user.is_admin is True
    assert response.status_code == 200
    helpers.check_menu(response=response, current_user=current_user)
    assert '<h3 class="color-text">Available colors</h3>' in response.text


def test_admin_colors_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/admin/colors` page
    THEN redirect to `/auth/login` page should occur
    """
    response = test_client.get(helpers.admin_colors_endpoint)

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
def test_admin_colors_view_post(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends POST request to `/admin/colors` page
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post(helpers.admin_colors_endpoint)

    assert response.status_code == 405
    assert helpers.method_not_allowed_h_tag in response.text
