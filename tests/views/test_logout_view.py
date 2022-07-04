from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_logout_view(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends GET request to `/logout` url
    THEN User should be logged out and redirect to `/` page should occur
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get("/logout")

    assert response.status_code == 302
    assert "Redirecting..." in response.text
    assert "/" == response.headers.get("Location", "")


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_logout_view_post(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends POST request to `/logout` url
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post("/logout")

    assert response.status_code == 405
    assert "Method Not Allowed" in response.text
