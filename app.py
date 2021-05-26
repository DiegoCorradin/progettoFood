from os import path
from flask import Flask, render_template, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from database.db import initialize_db, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, LoginManager, login_user, login_required, logout_user, current_user
from database.models import Users

app = Flask(__name__)
DB_NAME = 'alimentazione.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
#db = SQLAlchemy(app)
initialize_db(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



@app.route("/")
def index():
    return render_template("layout.html")


@app.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)

class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=30)]
    )
    remember = BooleanField("remember me")


class RegisterForm(FlaskForm):
    email = StringField(
        "email",
        validators=[InputRequired(), Email(message="invalid email"), Length(max=50)],
    )
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=30)]
    )



@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = Users(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login')

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('dashboard')

        return "<h1> invalid username or password </h1>"

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #db.session.commit()
        
    app.run(debug=True)
    
