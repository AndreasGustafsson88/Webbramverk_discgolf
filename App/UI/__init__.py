from bson import ObjectId
from flask import Flask, render_template, make_response, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import json
from App.Controller.courses_controller import get_all_names, get_one_course, update_favorite_courses, get_course_by_id
from App.Controller.my_chart_controller import return_random
from App.Controller.users_controller import get_all_friends, get_users, get_user_by_email, get_user_by_username, \
    get_user, add_user, find_unique, add_friend, get_all_users, delete_friend, add_friend_request, delete_friend_request
from App.Data.Models.flaskform import SignInForm, SignUpForm
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
    return find_unique(_id=ObjectId(_id))


@app.route('/', methods=["POST", "GET"])
def index():
    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = find_unique(user_name=username)

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

        add_user(full_name=form.full_name.data, user_name=form.user_name.data,
                 password=generate_password_hash(form.password.data, "sha256", ), email=form.email.data)

        return redirect(url_for("index"))
    return render_template("signup.html", form=form)


@app.route('/log_out', methods=['GET'])
def log_out():
    logout_user()
    return redirect(url_for("index"))


@app.route('/courses', methods=["POST", "GET"])
def courses():
    if request.method == "POST":
        if "loading" in request.form:
            favorites = [get_course_by_id(course).name for course in current_user.favourite_courses]
            response = app.response_class(
                response=json.dumps({"favorites": favorites}),
                status=200,
                mimetype="application/json"
            )
            return response
        if "course" in request.form:
            course_name = request.form["course"]
            if update_favorite_courses(course_name, current_user):
                message = "Course added to favorites"
            else:
                message = "Course removed from favorites"
            response = app.response_class(
                response=json.dumps(message),
                status=200,
                mimetype="application/json"
            )
            return response

    all_courses = get_all_names()
    return render_template('courses.html', all_courses=json.dumps(all_courses))


@app.route('/scorecard')
def scorecard():
    friends = get_all_friends(current_user)

    all_courses = get_all_names()

    return render_template("create_scorecard.html", all_courses=all_courses, friends=friends, current_user=current_user)


@app.route("/scorecard/play")
def scorecard_play():
    players = get_users(request.args.get("players").replace("[", "").replace("]", "").replace('"', '').split(","))
    course = get_one_course(request.args.get("course"))

    for player in players:
        player.hcp = player.player_hcp(course)

    return render_template("scorecard.html", course=course, players=players)


@app.route('/profile_page/<user_name>', methods=["GET", "POST", "DELETE"])
@login_required
def profile_page(user_name):
    if request.method == "POST":
        visited_user_id = request.form['id']

        if request.form['action'] == 'post accept_request':
            request_user = get_user(user_name=request.form['request_username'])
            message = add_friend(current_user, request_user._id, from_request=True)
            return app.response_class(**message)

        if request.form['action'] == 'post add_friend':
            visited_user = get_user(_id=ObjectId(visited_user_id))

            message = add_friend(current_user, visited_user_id)
            add_friend_request(current_user, visited_user)

            response = app.response_class(**message)
            return response



    if request.method == "DELETE":
        friend = get_user(user_name=request.form['username'])

        if request.form['action'] == "action remove":
            message = delete_friend(current_user, friend._id)
            response = app.response_class(**message)
            return response

        if request.form['action'] == 'action decline_request':
            message = delete_friend_request(current_user, friend._id)
            return app.response_class(**message)


    visited_profile = get_user_by_username(user_name)
    all_users = get_all_users()
    return render_template('profile_page.html', visited_profile=visited_profile, all_users=all_users)


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, return_random()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
