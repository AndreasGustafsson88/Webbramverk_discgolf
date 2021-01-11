from bson import ObjectId
from flask import Flask, render_template, make_response, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import json
from App.Controller.courses_controller import get_all_names, get_one_course
from App.Controller.my_chart_controller import return_random
from App.Controller.users_controller import get_all_friends, get_users, get_user_by_email, get_user_by_username, \
get_user, add_user
from App.Data.Models.courses import Course
from App.Data.Models.flaskform import SignInForm, SignUpForm
from App.Data.Models.users import User
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__,
            static_url_path="",
            static_folder="")

app.config["SECRET_KEY"] = "supersecret, don't tell"
login_manager = LoginManager()
login_manager.login_view = "index"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(_id):
    return User.find_unique(_id=ObjectId(_id))


@app.route('/', methods=["POST", "GET"])
def index():
    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.find_unique(user_name=username)

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("profile_page", user_name=current_user.user_name))

    return render_template("index.html", form=form)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        password = form.password.data
        confirmed_password = form.confirm_password.data

        if password != confirmed_password:
            flash("password are not the same")
            return redirect(url_for("signup"))

        if get_user(email=form.email.data):
            flash("Email already exists")
            return redirect(url_for("signup"))

        if get_user(user_name=form.user_name.data):
            flash("Username already exists")
            return redirect(url_for("signup"))

        # if get_user_by_email(form.email.data):
        #     flash("Email already exists")
        #     return redirect(url_for("signup"))
        #
        # if get_user_by_username(form.user_name.data):
        #     flash("Username already exists")
        #     return redirect(url_for("signup"))

        add_user(full_name=form.full_name.data, user_name=form.user_name.data, password=generate_password_hash(form.password.data, "sha256", ), email=form.email.data)

        return redirect(url_for("index"))
    return render_template("signup.html", form=form)


@app.route('/log_out', methods=['GET'])
def log_out():
    logout_user()
    return redirect(url_for("index"))


@app.route('/courses')
def courses():
    return render_template("courses.html")


@app.route('/scorecard')
def scorecard():

    friends = get_all_friends(current_user)



    all_courses = get_all_names()

    return render_template("create_scorecard.html", all_courses=all_courses, friends=friends, current_user=current_user)



@app.route("/scorecard/play")
def scorecard_play():
    '''course = {
        "Gässlösa Discgolfcenter": {
            1: ["Par 3", 156],
            2: ["Par 3", 76],
            3: ["Par 4", 145],
            4: ["Par 3", 96],
            5: ["Par 3", 75],
            6: ["Par 3", 89],
            7: ["Par 4", 201],
            8: ["Par 3", 79],
            9: ["Par 3", 114],
        }
    }'''
    # course = request.args.get("course")
    players = get_users(request.args.get("players").replace("[", "").replace("]", "").replace('"', '').split(","))
    course = get_one_course(request.args.get("course"))

    for player in players:
        player.hcp = player.player_hcp(course)

    return render_template("scorecard.html", course=course, players=players)


@app.route('/profile_page', methods=["GET", "POST"])
@login_required
def profile_page():
    return render_template('profile_page.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, return_random()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
