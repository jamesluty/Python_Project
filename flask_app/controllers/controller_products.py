from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_product import Product


@app.route("/category/<string:category>")
def category(category):
    all_products = Product.get_products({'category': category})
    category = category.capitalize()
    if category == 'Car_seats':
        category = "Car Seats"
    return render_template("category.html", category=category, all_products=all_products)

@app.route("/sell")
def sell_product():
    return render_template("sell.html")