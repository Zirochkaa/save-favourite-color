from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests.helpers import check_menu


@pytest.mark.parametrize(
    "client",
    (
        "test_client",
        "test_client_with_logged_in_user",
        "test_client_with_logged_in_admin",
    )
)
def test_page_not_found(client: str, request: FixtureRequest):
    """
    GIVEN an (AnonymousUser, User, Admin User)
    WHEN an (AnonymousUser, User, Admin User) sends GET request to page that doesn't exist
    THEN `404` error code should be returned along with template for 404 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get("/some_wrong_url")

    assert response.status_code == 404
    check_menu(response=response, current_user=current_user)
    assert '<h3 class="color-text">Page not found ;(</h3>' in response.text
