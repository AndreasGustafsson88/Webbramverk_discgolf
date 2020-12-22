from flask import Flask, render_template

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