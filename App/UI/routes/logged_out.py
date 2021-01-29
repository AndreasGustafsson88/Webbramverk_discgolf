from flask import Blueprint
from bson import ObjectId
from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from App.Controller.users_controller import get_user, add_user, find_unique
from App.Data.Models.courses import Course
from App.Data.Models.flaskform import SignInForm, SignUpForm
from flask_login import login_user, current_user

from App.Data.Models.users import User
from App.UI import login

logged_out = Blueprint("logged_out", __name__)


@login.user_loader
def load_user(_id):
    return find_unique(_id=ObjectId(_id))


@logged_out.route('/', methods=["POST", "GET"])
def index():
    # måns = User.find(user_name='MansMcMan').first_or_none()
    # wily = User.find(user_name='WillyMcDrive').first_or_none()
    # c = User.find(user_name='CMcCrush').first_or_none()
    # andy = User.find(user_name='Mcbeast').first_or_none()
    # måns.history = []
    # wily.history = []
    # c.history = []
    # andy.history = []
    #
    # måns.save()
    # wily.save()
    # c.save()
    # andy.save()

    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = find_unique(user_name=username)

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
            flash("password are not the same")
            return redirect(url_for("logged_out.signup"))

        if get_user(email=form.email.data):
            flash("Email already exists")
            return redirect(url_for("logged_out.signup"))

        if get_user(user_name=form.user_name.data):
            flash("Username already exists")
            return redirect(url_for("logged_out.signup"))

        add_user(full_name=form.full_name.data, user_name=form.user_name.data,
                 password=generate_password_hash(form.password.data, "sha256", ), email=form.email.data)

        return redirect(url_for("logged_out.index"))
    return render_template("signup.html", form=form)
