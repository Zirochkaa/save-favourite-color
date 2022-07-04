from typing import Union

from flask_login import AnonymousUserMixin, UserMixin


def check_menu(response, current_user: Union[UserMixin, AnonymousUserMixin]):
    assert '<a class="nav-link" style="color:#fcc729" href="/">Home</a>' in response.text
    assert '<a class="nav-link" style="color:#fcc729" href="/profile">Profile</a>' in response.text

    if isinstance(current_user, AnonymousUserMixin):
        assert '<a class="nav-link color-text" href="/login">Log in</a>' in response.text
        assert '<a class="nav-link color-text" href="/signup">Sign up</a>' in response.text
        assert '<a class="nav-link color-text" href="/settings">Settings</a>' not in response.text
        assert '<a class="nav-link color-text" href="/logout">Log out</a>' not in response.text
    else:
        assert '<a class="nav-link color-text" href="/login">Log in</a>' not in response.text
        assert '<a class="nav-link color-text" href="/signup">Sign up</a>' not in response.text
        assert '<a class="nav-link color-text" href="/settings">Settings</a>' in response.text
        assert '<a class="nav-link color-text" href="/logout">Log out</a>' in response.text
        assert f'<a class="nav-link color-text">Hello, {current_user.username}</a>' in response.text
