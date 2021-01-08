from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired


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


class SignUpForm(FlaskForm):
    full_name = StringField(
        "full_name",
        [InputRequired()],
        render_kw={
            "placeholder": "Full name"
        })
    user_name = StringField(
        "user_name",
        [DataRequired()],
        render_kw={
            "placeholder": "Username"
        })
    email = StringField(
        "email",
        [DataRequired()],
        render_kw={
            "placeholder": "Email"
        })
    password = PasswordField(
        "password",
        [DataRequired()],
        render_kw={
            "placeholder": "Password"
        })
    confirm_password = PasswordField(
        "conform_password",
        [DataRequired()],
        render_kw={
            "placeholder": "Repeat password"
        })
    submit = SubmitField(
        "submit",
        render_kw={"value": "Signup"}
    )