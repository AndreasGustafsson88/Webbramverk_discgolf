from flask import Flask, render_template

app = Flask(__name__,
            static_url_path="",
            static_folder="/app/UI/static")


@app.route('/')
def index():

    return render_template("base_logged_out.html")


if __name__ == '__main__':
    app.run(debug=True)
