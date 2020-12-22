from flask import Flask, render_template

app = Flask(__name__,
            static_url_path="",
            static_folder="")

names = ["Andreas", "Christoffer", "Måns", "William"]


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

    return render_template("scorecard.html")


@app.route('/autocomplete')
def autocomplete():

    return render_template("autocomplete.html", names=names)
