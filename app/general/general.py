from flask import Blueprint, render_template

from app.templates_paths import home_template_path, not_found_template_path

general_bp = Blueprint("general", __name__, template_folder='templates', static_folder='static',
                       static_url_path='/assets')


@general_bp.route("/", methods=["GET"])
def home():
    return render_template(home_template_path)


@general_bp.app_errorhandler(404)
def invalid_route(e):
    return render_template(not_found_template_path), 404
