from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests.helpers import check_menu


def test_profile_view(test_login_client: FlaskLoginClient):
    """
    GIVEN a User
    WHEN a User sends GET request to `/profile` page
    THEN `/profile` page should be shown
    """
    response = test_login_client.get("/profile")

    assert response.status_code == 200
    check_menu(response=response, current_user=current_user)
    assert f"Your favourite color is {current_user.favourite_color}" in response.text


def test_profile_view_anonymous_user(test_client: FlaskClient):
    """
    GIVEN an AnonymousUser
    WHEN an AnonymousUser sends GET request to `/profile` page
    THEN redirect to `/login` page should occur
    """
    response = test_client.get("/profile")

    assert response.status_code == 302
    assert "Redirecting..." in response.text
    assert "/login" in response.headers.get("Location", "")


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_profile_view_post(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends POST request to `/profile` page
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post("/profile")

    assert response.status_code == 405
    assert "Method Not Allowed" in response.text
