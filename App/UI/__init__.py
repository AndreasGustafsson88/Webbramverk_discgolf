from flask import Flask
from flask_login import LoginManager
from App.UI.routes.jinja2_filters import json_decode
from config import Config
import os


# Globally accessible libraries
login = LoginManager()


def create_app():
    templates_folder = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=templates_folder,
        static_url_path='',
        static_folder=os.path.abspath(os.path.dirname(__file__)) + '/static')
    app.config.from_object(Config)

    # Initialize Plugins
    login.init_app(app)

    with app.app_context():
        # Imports
        from App.UI.routes import logged_out as logged_out_blueprint
        from App.UI.routes import logged_in as logged_in_blueprint
        from App.UI.routes import errors as error_blueprints
        from App.UI.routes import courses_bp as courses_bp_blueprint
        from App.UI.routes import scorecards as scorecard_blueprint
        from App.UI.routes import profile as profile_blueprint

        login.login_view = "logged_out.index"

        # Register blueprints
        app.register_blueprint(error_blueprints.error)
        app.register_blueprint(logged_out_blueprint.logged_out)
        app.register_blueprint(logged_in_blueprint.logged_in)
        app.register_blueprint(courses_bp_blueprint.courses_bp)
        app.register_blueprint(scorecard_blueprint.scorecards)
        app.register_blueprint(profile_blueprint.profile)

        # Register Jinja2 filters
        app.jinja_env.filters['json_decode'] = json_decode

        return app
