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

if __name__ == '__main__':
    app.run(debug=True)
