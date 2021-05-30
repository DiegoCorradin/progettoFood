from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #isntazia db object, nessuna app associata

def initialize_db(app):
    db.init_app(app)

