from flask import Flask, render_template, request

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


@app.route('/profile_page')
def profile_page():

    return render_template("profile_page.html")


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

