from flask import redirect, url_for, Blueprint
from flask_login import logout_user, login_required

logged_in = Blueprint('logged_in', __name__)


@logged_in.route('/log_out', methods=['GET'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("logged_out.index"))
