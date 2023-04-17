from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Color
from app.templates_paths import profile_template_path, settings_template_path

profile_bp = Blueprint("profile", __name__, template_folder='templates', static_folder='static',
                       static_url_path='/assets', url_prefix='/profile')


profile_endpoint = "profile.profile"


@profile_bp.route("/", methods=["GET"])
@login_required
def profile():
    return render_template(profile_template_path)


@profile_bp.route("/settings/color", methods=["GET"])
@login_required
def settings():
    return render_template(settings_template_path, colors=Color.get_all_active_colors())


@profile_bp.route("/settings/color", methods=["POST"])
@login_required
def settings_post():
    favourite_color = request.form.get("color")

    if not Color.check_exists(color=favourite_color):
        flash(f"We do not support such ({favourite_color}) color yet")
        colors = Color.get_all_active_colors()
        return render_template(settings_template_path, colors=colors)

    current_user.save_favourite_color(favourite_color=favourite_color)
    return redirect(url_for(profile_endpoint))
