from typing import Union

import pytest
from _pytest.fixtures import FixtureRequest
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient, current_user

from tests.helpers import check_menu


@pytest.mark.parametrize("client", ["test_client", "test_login_client"])
def test_page_not_found(client: str, request: FixtureRequest):
    """
    GIVEN a (User, AnonymousUser)
    WHEN a (User, AnonymousUser) sends GET request to page that doesn't exist
    THEN `404` error code should be returned along with template for 404 page
    """
    client: Union[FlaskClient, FlaskLoginClient] = request.getfixturevalue(client)
    response = client.get("/some_wrong_url")

    assert response.status_code == 404
    check_menu(response=response, current_user=current_user)
    assert '<h3 class="color-text">Page not found ;(</h3>' in response.text
