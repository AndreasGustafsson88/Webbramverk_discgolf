from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class SettingsForm(FlaskForm):
    IMAGES = list('jpg jpe jpeg png gif svg bmp'.split())
    profile_picture_input = FileField("images", validators=[
        FileAllowed(IMAGES, message="img files only!")
    ],
        render_kw={
            "placeholder": "Profile Picture",
        }
    )
    user_name = StringField(
        "user_name",
        render_kw={
            "placeholder": "New username (Optional)"
        })
    email = StringField(
        "email",
        render_kw={
            "placeholder": "New email (Optional)",
            })
    password = PasswordField(
        'password',
        render_kw={
            "placeholder": "New password (Optional)"
        })
    confirm_password = PasswordField(
        "conform_password",
        validators=[EqualTo('password')],
        render_kw={
            "placeholder": "Repeat password"
        })
    current_password = PasswordField(
        "current_password",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Current password"
        })
    submit = SubmitField(
        "submit",
        render_kw={"value": "Update"}
    )

