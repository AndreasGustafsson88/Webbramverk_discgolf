from flask import Blueprint
from bson import ObjectId
from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from App.Controller import users_controller as uc
from App.UI.static.flaskform.sign_in_form import SignInForm
from App.UI.static.flaskform.sign_up_form import SignUpForm
from flask_login import login_user, current_user
from App.UI import login

logged_out = Blueprint("logged_out", __name__)


@login.user_loader
def load_user(_id):
    return uc.find_unique(_id=ObjectId(_id))


@logged_out.route('/', methods=["POST", "GET"])
def index():

    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = uc.find_unique(user_name=username)

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("profile.profile_page", user_name=current_user.user_name))

    return render_template("index.html", form=form)


@logged_out.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        password = form.password.data
        confirmed_password = form.confirm_password.data

        if password != confirmed_password:
            flash("Password are not the same")
            return redirect(url_for("logged_out.signup"))

        if uc.get_user(email=form.email.data):
            flash("Email already exists")
            return redirect(url_for("logged_out.signup"))

        if uc.get_user(user_name=form.user_name.data):
            flash("Username already exists")
            return redirect(url_for("logged_out.signup"))

        uc.add_user(full_name=form.full_name.data, user_name=form.user_name.data,
                 password=generate_password_hash(form.password.data, "sha256", ), email=form.email.data)

        return redirect(url_for("logged_out.index"))
    return render_template("signup.html", form=form)
