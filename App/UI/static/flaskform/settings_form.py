from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SettingsForm(FlaskForm):
    IMAGES = list('jpg jpe jpeg png gif svg bmp'.split())
    profile_picture = FileField("images", validators=[
        FileAllowed(IMAGES, message="img files only!")
    ],
        render_kw={
            "placeholder": "Profile Picture"
        }
    )
    user_name = StringField(
        "user_name",
        [DataRequired()],
        render_kw={
            "placeholder": "New username (Optional)"
        })
    email = StringField(
        "email",
        [DataRequired()],
        render_kw={
            "placeholder": "New email (Optional)"
        })
    password = PasswordField(
        'password',
        [DataRequired()],
        render_kw={
            "placeholder": "New password (Optional)"
        })
    confirm_password = PasswordField(
        "conform_password",
        validators=[DataRequired(), EqualTo('password')],
        render_kw={
            "placeholder": "Repeat password"
        })
    submit = SubmitField(
        "submit",
        render_kw={"value": "Update"}
    )
