from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/home")
def child():
    return render_template("child.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)

