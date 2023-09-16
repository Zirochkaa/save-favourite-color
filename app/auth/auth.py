from urllib.parse import urlparse, parse_qs

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app.models import Color, User
from app.templates_paths import login_template_path, signup_template_path, after_signup_template_path

auth_bp = Blueprint("auth", __name__, template_folder='templates', static_folder='static',
                    static_url_path='/assets', url_prefix='/auth')


profile_endpoint = "profile.profile"
home_endpoint = "general.home"


@auth_bp.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated is True:
        return redirect(url_for(profile_endpoint))

    return render_template(login_template_path)


@auth_bp.route("/login", methods=["POST"])
def login_post():
    if current_user.is_authenticated is True:
        return redirect(url_for(profile_endpoint))

    username = request.form.get("username")
    password = request.form.get("password")
    remember = False  # TODO Get `remember` value from request form.

    # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
    if not username or not username.strip() or not password or not password.strip():
        flash("Username/password can not be empty")
        return render_template(login_template_path), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password=password):
        flash("User with such username/password does not exist")
        return render_template(login_template_path), 400

    was_logged_in = login_user(user, remember=remember)
    if was_logged_in is True:
        parsed_url = urlparse(request.headers.get('referer', ''))
        parsed_query = parse_qs(parsed_url.query)

        if parsed_query.get('next'):
            return redirect(parsed_query['next'][0])

        return redirect(url_for(profile_endpoint))

    flash("Something went wrong during login process")
    return render_template(login_template_path), 400


@auth_bp.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated is True:
        logout_user()

    return redirect(url_for(home_endpoint))


@auth_bp.route("/signup", methods=["GET"])
def signup():
    if current_user.is_authenticated is True:
        return redirect(url_for(profile_endpoint))

    return render_template(signup_template_path, colors=Color.get_all_active_colors())


@auth_bp.route("/signup", methods=["POST"])
def signup_post():
    if current_user.is_authenticated is True:
        return redirect(url_for(profile_endpoint))

    colors = Color.get_all_active_colors()
    username = request.form.get("username")
    password = request.form.get("password")
    favourite_color = request.form.get("color")

    # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
    if not username or not username.strip() or not password or not password.strip():
        flash("Username/password can not be empty")
        return render_template(signup_template_path, colors=colors), 400

    # Check that user with this username already exists.
    user = User.query.filter_by(username=username).first()
    if user:
        flash("User with such username already exist")
        return render_template(signup_template_path, colors=colors), 400

    # Since we had limited amount of colors, we need to check that color we got in form is from that limited amount.
    if not Color.check_exists(color=favourite_color):
        flash(f"We do not support such ({favourite_color}) color yet")
        return render_template(signup_template_path, colors=colors), 400

    User.signup(username=username, password=password, favourite_color=favourite_color)
    return render_template(after_signup_template_path)
