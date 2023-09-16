from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import Color, User
from app.templates_paths import not_found_template_path, admin_colors_template_path, admin_users_template_path

admin_bp = Blueprint("admin", __name__, template_folder='templates', static_folder='static',
                     static_url_path='/assets', url_prefix='/admin')


@admin_bp.route("/colors", methods=["GET"])
@login_required
def colors():
    if current_user.is_admin is False:
        return render_template(not_found_template_path), 404

    return render_template(admin_colors_template_path, colors=Color.get_all_colors())


@admin_bp.route("/users", methods=["GET"])
@login_required
def users():
    if current_user.is_admin is False:
        return render_template(not_found_template_path), 404

    return render_template(admin_users_template_path, users=User.get_all_users())
