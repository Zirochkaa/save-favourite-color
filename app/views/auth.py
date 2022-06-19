from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import Color, User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated is True:
        return redirect(url_for("main.profile"))

    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = False  # TODO Get `remember` value from request form.

    # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
    if not username or not username.strip() or not password or not password.strip():
        flash("Username/password can't be empty")
        return render_template("login.html")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password=password):
        flash("User with such username/password doesn't exist")
        return render_template("login.html")

    was_logged_in = login_user(user, remember=remember)
    if was_logged_in is True:
        return redirect(url_for("main.profile"))

    flash("User with such username/password doesn't exist")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/signup", methods=["GET"])
def signup():
    if current_user.is_authenticated is True:
        return redirect(url_for("main.profile"))

    colors = Color.get_all_active_colors()
    return render_template("signup.html", colors=colors)


@auth.route("/signup", methods=["POST"])
def signup_post():
    colors = Color.get_all_active_colors()
    username = request.form.get("username")
    password = request.form.get("password")
    favourite_color = request.form.get("color")

    # `username` or `password` can't be empty. Also, they can't consist only from whitespaces.
    if not username or not username.strip() or not password or not password.strip():
        flash("Username/password can't be empty")
        return render_template("signup.html", colors=colors)

    # Check that user with this username already exists.
    user = User.query.filter_by(username=username).first()
    if user:
        flash("User with such username already exist")
        return render_template("signup.html", colors=colors)

    # Since we had limited amount of colors, we need to check that color we got in form is from that limited amount.
    if not Color.check_exists(color=favourite_color):
        flash(f"We don't support '{favourite_color}' color yet")
        return render_template("signup.html", colors=colors)

    User.signup(username=username, password=password, favourite_color=favourite_color)
    return render_template("after_signup.html")
