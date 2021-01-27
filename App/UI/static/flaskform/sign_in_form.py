from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired



class SignInForm(FlaskForm):
    username = StringField(
        "username",
        [DataRequired(message="Please enter your username")],
        render_kw={
            "placeholder": "Username",
            "style": "height: 100%; width: 100%"
        }
    )
    password = PasswordField(
        "password",
        [DataRequired(message="Please enter a password.")],
        render_kw={
            "placeholder": "Password",
            "style": "height: 100%; width: 100%"
        }
    )
    submit = SubmitField(
        "submit",
        render_kw={
            "value": "Login",
            "style": "height: 100%; width: 100%"
        }
    )
