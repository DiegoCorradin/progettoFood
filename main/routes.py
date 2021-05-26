from flask import Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("layout.html")


@main.route("/index")
def index():
    return render_template("index.html")