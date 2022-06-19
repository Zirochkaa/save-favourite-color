from flask import Blueprint, render_template
from flask_login import login_required


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html")


@main.app_errorhandler(404)
def invalid_route(e):
    return render_template("404_page.html"), 404
