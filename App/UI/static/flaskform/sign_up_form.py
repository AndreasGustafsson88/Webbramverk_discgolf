from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired


def forbidden_characters(c=None):
    if c is None:
        c = []

    message = f"Can't contain any of the following characters: {','.join(c)}"

    def _forbidden_characters(Flaskform, field):
        pattern = field.data
        for p in pattern:
            if p in c:
                raise ValueError(message)

    return _forbidden_characters


class SignUpForm(FlaskForm):
    full_name = StringField(
        "full_name",
        [InputRequired()],
        render_kw={
            "placeholder": "Full name"
        })
    user_name = StringField(
        "user_name",
        [DataRequired(), forbidden_characters(["|"])],
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
