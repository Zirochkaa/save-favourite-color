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
def test_home_view(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends GET request to `/` page
    THEN `/` page should be shown
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get(helpers.home_endpoint)

    assert response.status_code == 200

    # We don't use `check_menu()` here because menu on `/` page looks the same for AnonymousUser, User and Admin User.
    assert helpers.home_a_tag in response.text
    assert helpers.profile_a_tag in response.text
    assert helpers.login_a_tag in response.text
    assert helpers.signup_a_tag in response.text
    assert helpers.settings_a_tag not in response.text
    assert helpers.logout_a_tag not in response.text

    assert '<h3 class="color-text">Do you often forget your favourite color?</h3>' in response.text
    assert '<h3 class="color-text">We will help you with this :)</h3>' in response.text
    assert '<h3 class="color-text">On this site you can save your favourite color and ' \
           'share it with friends.</h3>' in response.text


@pytest.mark.parametrize(
    "client",
    (
        "test_client",
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_home_view_post(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends POST request to `/` page
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post(helpers.home_endpoint)

    assert response.status_code == 405
    assert helpers.method_not_allowed_h_tag in response.text
