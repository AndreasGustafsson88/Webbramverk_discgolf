from flask import render_template, Blueprint

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def not_found_error(errors):
    return render_template('404.html'), 404


@error.app_errorhandler(500)
def internal_error(errors):
    return render_template('500.html'), 500


@error.app_errorhandler(413)
def file_too_big(errors):
    return render_template('413.html'), 413
