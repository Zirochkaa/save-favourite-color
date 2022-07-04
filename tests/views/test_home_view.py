from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_home_view(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends GET request to `/` page
    THEN `/` page should be shown
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get("/")

    assert response.status_code == 200

    # We don't use `check_menu()` here because menu on `/` page looks the same for both User and AnonymousUser.
    assert '<a class="nav-link" style="color:#fcc729" href="/">Home</a>' in response.text
    assert '<a class="nav-link" style="color:#fcc729" href="/profile">Profile</a>' in response.text
    assert '<a class="nav-link color-text" href="/login">Log in</a>' in response.text
    assert '<a class="nav-link color-text" href="/signup">Sign up</a>' in response.text
    assert '<a class="nav-link color-text" href="/settings">Settings</a>' not in response.text
    assert '<a class="nav-link color-text" href="/logout">Log out</a>' not in response.text

    assert '<h3 class="color-text">Do you often forget your favourite color?</h3>' in response.text
    assert '<h3 class="color-text">We will help you with this :)</h3>' in response.text
    assert '<h3 class="color-text">On this site you can save your favourite color and ' \
           'share it with friends.</h3>' in response.text


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_home_view_post(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends POST request to `/` page
    THEN `405` error code should be returned along with template for 405 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.post("/")

    assert response.status_code == 405
    assert "<h1>Method Not Allowed</h1>" in response.text
