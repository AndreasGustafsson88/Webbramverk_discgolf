import os
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
from App.Controller.my_encoder import MyEncoder
from App.Controller import courses_controller as cc
from App.Controller import scorecards_controller as sc
from App.Controller import users_controller as uc
from App.Data.Models.flaskform import SignInForm, SignUpForm, SettingsForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from App.Data.Models.scorecards import Scorecard


app = Flask(__name__,
            static_url_path="",
            static_folder="")


app.config["SECRET_KEY"] = "supersecret, don't tell"
sources_root = os.path.abspath(os.path.dirname('App'))
#todo prata i gruppen var vi vill lagra profilbilder.
UPLOAD_FOLDER = os.path.join(sources_root, 'App/UI/static/assets/img/profile_pictures/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.login_view = "index"
login_manager.init_app(app)

@app.template_filter("to_console")
def to_console(text):
    print(str(text))
    return ""


@app.template_filter('json_decode')
def json_decode(o):
    if isinstance(o, Scorecard):
        b = vars(o)
        b['_id'] = str(b['_id'])
        return json.dumps(b)
    else:
        for history in o:
            history[3] = str(history[3])
        return json.dumps(o)

app.jinja_env.filters['json_decode'] = json_decode

@login_manager.user_loader
def load_user(_id):
    return uc.find_unique(_id=ObjectId(_id))


@app.route('/', methods=["POST", "GET"])
def index():
    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = uc.find_unique(user_name=username)

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

        if uc.get_user(email=form.email.data):
            flash("Email already exists")
            return redirect(url_for("signup"))

        if uc.get_user(user_name=form.user_name.data):
            flash("Username already exists")
            return redirect(url_for("signup"))

        uc.add_user(full_name=form.full_name.data, user_name=form.user_name.data,
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
            favorites = [cc.get_course_by_id(course).name for course in current_user.favourite_courses]
            response = app.response_class(
                response=json.dumps({"favorites": favorites}),
                status=200,
                mimetype="application/json"
            )
            return response
        if "course" in request.form:
            course_name = request.form["course"]
            if cc.update_favorite_courses(course_name, current_user):
                message = "Course added to favorites"
            else:
                message = "Course removed from favorites"
            response = app.response_class(
                response=json.dumps(message),
                status=200,
                mimetype="application/json"
            )
            return response

    all_courses = [[course.name, len(course.history)] for course in cc.get_all_courses()]
    return render_template('courses.html', all_courses=json.dumps(all_courses))


@app.route('/scorecard', methods=["POST", "GET"])
def scorecard():
    if request.method == 'POST':
        course = cc.get_one_course(request.form["course"])
        response = app.response_class(
            response=json.dumps(course.holes[0]),
            status=200,
            mimetype="application/json"
        )
        return response
    friends = uc.get_all_friends(current_user)

    all_courses = cc.get_all_names()

    return render_template("create_scorecard.html", all_courses=all_courses, friends=friends, current_user=current_user)


@app.route("/scorecard/play", methods=['GET', 'POST'])
def scorecard_play():
    if request.method == 'POST':
        player_summary = json.loads(request.form['p_summary'])
        message = uc.add_round(player_summary)
        response = app.response_class(
            response=json.dumps(message),
            status=200,
            mimetype="application/json"
        )
        return response

    players = uc.get_users(request.args.get("players").replace("[", "").replace("]", "").replace('"', '').split(","))
    course = cc.get_one_course(request.args.get("course"))
    rated = True if request.args.get("rated")=="true" else False
    multi = int(request.args.get("multi"))

    for player in players:
        player.hcp = uc.calculate_extra_strokes(player, course)

    sc.create_scorecard(course, players, multi, rated)
    uc.add_incomplete_scorecard(scorecard, players)

    return render_template("scorecard.html", round_summary=scorecard)


@app.route('/profile_page/<user_name>', methods=["GET", "POST"])
@login_required
def profile_page(user_name):
    if request.method == "POST":

        if 'button' in request.form:
            scorecard = sc.get_scorecard(_id=ObjectId(request.form['button']))
            return redirect(url_for('scorecard_history', scorecard_id=scorecard._id))

        visited_user_id = request.form['id']

        if request.form['action'] == 'post accept_request':
            request_user = uc.get_user(user_name=request.form['request_username'])
            message = uc.add_friend(current_user, request_user._id, from_request=True)
            return app.response_class(**message)

        if request.form['action'] == 'post add_friend':
            visited_user = uc.get_user(_id=ObjectId(visited_user_id))

            message = uc.add_friend(current_user, visited_user_id)
            uc.add_friend_request(current_user, visited_user)

            response = app.response_class(**message)
            return response
    settings_form = SettingsForm()
    visited_profile = uc.get_user_by_username(user_name)
    visited_profile.history = json.dumps(visited_profile.history, cls=MyEncoder)
    all_users = uc.get_all_users()
    favorite_courses = [cc.get_course_by_id(course_id).name for course_id in visited_profile.favourite_courses]
    return render_template('profile_page.html', visited_profile=visited_profile, all_users=all_users,
                           form=settings_form, favorite_courses=favorite_courses)


@app.route('/profile_page/<user_name>', methods=["DELETE"])
def profile_page_delete(user_name):
    if request.method == "DELETE":
        friend = uc.get_user(user_name=request.form['username'])


        if request.form['action'] == "action remove":
            message = uc.delete_friend(current_user, friend._id)
            response = app.response_class(**message)
            return response

        if request.form['action'] == 'action decline_request':
            message = uc.delete_friend_request(current_user, friend._id)
            return app.response_class(**message)


@app.route('/profile_page/settings', methods=['POST'])
def profile_page_update():
    settings_form = SettingsForm()
    if settings_form.validate_on_submit():
        if settings_form.profile_picture.data is not None:
            file_name = settings_form.user_name.data.strip().replace(' ', '_')
            settings_form.profile_picture.data.save(os.path.join(UPLOAD_FOLDER, f'{file_name}.jpg'))
            current_user.profile_picture = "../static/assets/img/profile_pictures/" + file_name + ".jpg"
            current_user.save()

        if uc.get_user(email=settings_form.email.data):
            flash("Email already exists")
            return redirect(url_for('profile_page', user_name=current_user.user_name))

        if uc.get_user(user_name=settings_form.user_name.data):
            flash("Username already exists")
            return redirect(url_for('profile_page', user_name=current_user.user_name))

        uc.update_profile(current_user, settings_form.profile_picture.data, settings_form.user_name.data,
                       settings_form.email.data, generate_password_hash(settings_form.password.data, "sha256"))
        return redirect(url_for('index'))


@app.route('/scorecard/<scorecard_id>', methods=['GET', 'POST', 'DELETE'])
def scorecard_history(scorecard_id):

    if request.method == 'POST':
        scorecard = sc.get_scorecard(_id=ObjectId(request.form['button']))

        return render_template('scorecard.html', round_summary=scorecard)

    if request.method == 'DELETE':

        scorecard = sc.get_scorecard(_id=ObjectId(json.loads(request.form['p_summary'])['_id']))

        uc.remove_incomplete_scorecard(scorecard)
        sc.delete_scorecard(scorecard)

        return 'Scorecard deleted'
    scorecard = sc.get_scorecard(_id=ObjectId(scorecard_id))
    return render_template('scorecard.html', round_summary=scorecard)

