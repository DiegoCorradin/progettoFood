from flask import Blueprint, request, redirect, url_for
from flask.templating import render_template
from sqlalchemy.sql.operators import nullsfirst_op
from database.models import Alimenti, Log
from database.db import db
from datetime import datetime
main = Blueprint('main', __name__)





@main.route("/")
def home():
    return render_template("layout.html")


@main.route('/create_log', methods=['POST'])
def create_log():
    date = request.form.get('date')

    log = Log(date=datetime.strptime(date, '%Y-%m-%d'))
    db.session.add(log)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log.id))

@main.route('/add', methods=['GET'])
def add():
    foods = Alimenti.query.all()
    return render_template('add.html', foods=foods, food=None)

@main.route('/add', methods=['POST'])
def add_post():
    food_name = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbs = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    food_id = request.form.get('food-id')

    if food_id:
        food = Alimenti.query.get_or_404(food_id)
        food.name= food_name
        food.proteins= proteins
        food.carbs= carbs
        food.fats= fats

    else: 
        new_Food = Alimenti(
            name=food_name,
            proteins=proteins,
            carbs=carbs, fats=fats
        )    

        db.session.add(new_Food)

    db.session.commit()
    return redirect(url_for('main.add'))


@main.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    food = Alimenti.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()

    return redirect(url_for('main.add'))


@main.route('/edit_food/<int:food_id>')
def edit_food(food_id):
    food = Alimenti.query.get_or_404(food_id)
    foods = Alimenti.query.all()
    return render_template('add.html', food=food, foods=foods)

@main.route("/view/<int:log_id>")
def view(log_id):
    log = Log.query.get_or_404(log_id)

    foods = Alimenti.query.all()

    totali = {
        'proteins' : 0,
        'carbs' : 0,
        'fats' : 0,
        'calories' : 0
    }

    for food in log.foods:
        totali['proteins'] += food.proteins
        totali['carbs'] += food.carbs
        totali['fats'] += food.fats
        totali['calories'] += food.calories

    return render_template("view.html", foods=foods, log=log, totali=totali)

@main.route("/add_food_to_log/<int:log_id>", methods=['POST'])
def add_food_to_log(log_id):
    log = Log.query.get_or_404(log_id)

    selected_food = request.form.get('food-select')

    food = Alimenti.query.get(int(selected_food))

    log.foods.append(food)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))

@main.route("/remove_food_from_log/<int:log_id>/<int:food_id>", methods=['GET'])
def remove_food_from_log(log_id, food_id):
    log = Log.query.get(log_id)
    food = Alimenti.query.get(food_id)

    log.foods.remove(food)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))