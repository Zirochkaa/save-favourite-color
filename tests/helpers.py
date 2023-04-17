from typing import Union

from flask_login import AnonymousUserMixin, UserMixin


# HTML `a` tags for nav bar
home_a_tag = '<a class="nav-link color-text" href="/">[Home]</a>'
profile_a_tag = '<a class="nav-link color-text" href="/profile/">[Profile]</a>'
login_a_tag = '<a class="nav-link color-text" href="/auth/login">[Log in]</a>'
signup_a_tag = '<a class="nav-link color-text" href="/auth/signup">[Sign up]</a>'
settings_a_tag = '<a class="nav-link color-text" href="/profile/settings/color">[Settings]</a>'
logout_a_tag = '<a class="nav-link color-text" href="/auth/logout">[Log out]</a>'
username_a_tag = '<a class="nav-link color-text">Hello, {username}</a>'


redirect_h_tag = "<h1>Redirecting...</h1>"
method_not_allowed_h_tag = "<h1>Method Not Allowed</h1>"


def check_menu(response, current_user: Union[UserMixin, AnonymousUserMixin]):
    assert home_a_tag in response.text
    assert profile_a_tag in response.text

    if isinstance(current_user, AnonymousUserMixin):
        assert login_a_tag in response.text
        assert signup_a_tag in response.text
        assert settings_a_tag not in response.text
        assert logout_a_tag not in response.text
    else:
        assert login_a_tag not in response.text
        assert signup_a_tag not in response.text
        assert settings_a_tag in response.text
        assert logout_a_tag in response.text
        assert username_a_tag.format(username=current_user.username) in response.text


# Admin endpoints
admin_panel_endpoint = "/admin/"

# Auth endpoints
login_endpoint = "/auth/login"
logout_endpoint = "/auth/logout"
signup_endpoint = "/auth/signup"

# General endpoints
home_endpoint = "/"

# Profile endpoints
profile_endpoint = "/profile/"
settings_endpoint = "/profile/settings/color"
