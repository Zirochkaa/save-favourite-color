from typing import Union

from flask_login import AnonymousUserMixin, UserMixin

# Admin endpoints
admin_colors_endpoint = "/admin/colors"
admin_users_endpoint = "/admin/users"

# Auth endpoints
login_endpoint = "/auth/login"
logout_endpoint = "/auth/logout"
signup_endpoint = "/auth/signup"

# General endpoints
home_endpoint = "/"

# Profile endpoints
profile_endpoint = "/profile/"
settings_endpoint = "/profile/settings/color"


# HTML `a` tags for nav bar
home_a_tag = f'<a class="nav-link color-text" href="{home_endpoint}">[Home]</a>'
profile_a_tag = f'<a class="nav-link color-text" href="{profile_endpoint}">[Profile]</a>'
login_a_tag = f'<a class="nav-link color-text" href="{login_endpoint}">[Log in]</a>'
signup_a_tag = f'<a class="nav-link color-text" href="{signup_endpoint}">[Sign up]</a>'
settings_a_tag = f'<a class="nav-link color-text" href="{settings_endpoint}">[Settings]</a>'
admin_colors_a_tag = f'<a class="dropdown-item color-text" href="{admin_colors_endpoint}">[Colors]</a>'
admin_users_a_tag = f'<a class="dropdown-item color-text" href="{admin_users_endpoint}">[Users]</a>'
logout_a_tag = f'<a class="nav-link color-text" href="{logout_endpoint}">[Log out]</a>'
username_a_tag = '<a class="nav-link color-text">Hello, {username}</a>'


redirect_h_tag = "<h1>Redirecting...</h1>"
method_not_allowed_h_tag = "<h1>Method Not Allowed</h1>"

page_not_found_h_tag = '<h3 class="color-text">Page not found ;(</h3>'


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

        if current_user.is_admin:
            assert admin_colors_a_tag in response.text
            assert admin_users_a_tag in response.text
