from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app.models import Color


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html")


@main.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("settings.html", colors=Color.get_all_active_colors())


@main.route("/settings", methods=["POST"])
@login_required
def settings_post():
    favourite_color = request.form.get("color")

    if not Color.check_exists(color=favourite_color):
        flash(f"We do not support such ({favourite_color}) color yet")
        colors = Color.get_all_active_colors()
        return render_template("settings.html", colors=colors)

    current_user.save_favourite_color(favourite_color=favourite_color)
    return render_template("profile.html")


@main.app_errorhandler(404)
def invalid_route(e):
    return render_template("404_page.html"), 404
