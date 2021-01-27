from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired

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
