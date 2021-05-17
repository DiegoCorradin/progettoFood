from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=30)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='invalid email') ,Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=30)])

@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/home")
def child():
    return render_template("child.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template("login.html", form=form)

@app.route("/signup")
def signup():
    form = RegisterForm()
    return render_template("signup.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)