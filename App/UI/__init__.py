from flask import Flask, render_template, make_response, request
from time import time
import json
from App.Controller.courses_controller import get_all_names, get_one_course
from App.Controller.my_chart_controller import return_random
from App.Controller.users_controller import get_all_friends, get_users
from App.Data.Models.courses import Course
from App.Data.Models.users import User

app = Flask(__name__,
            static_url_path="",
            static_folder="")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/courses')
def courses():
    return render_template("courses.html")


@app.route('/scorecard')
def scorecard():

    current_user = User.find(user_name="Mcbeast").first_or_none()
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
def profile_page():
    return render_template('profile_page.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, return_random()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
