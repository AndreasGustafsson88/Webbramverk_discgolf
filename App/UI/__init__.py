from flask import Flask, render_template, make_response
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

    return render_template("scorecard.html")


@app.route('/profile_page', methods=["GET", "POST"])
def main():
    return render_template('profile_page.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, return_random()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
