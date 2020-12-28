from flask import Flask, render_template, make_response, request
from time import time
import json
from App.Controller.my_chart_controller import return_random

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

    return render_template("create_scorecard.html")


@app.route("/scorecard/play")
def scorecard_play():
    course = {
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
    }
    # course = request.args.get("course")
    players = request.args.get("players").replace("[", "").replace("]", "").split(",")

    course = course["Gässlösa Discgolfcenter"]

    return render_template("scorecard.html", course=course, players=players)


@app.route('/profile_page', methods=["GET", "POST"])
def main():
    return render_template('profile_page.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, return_random()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
