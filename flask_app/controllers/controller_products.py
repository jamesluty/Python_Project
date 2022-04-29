from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_product import Product


@app.route("/category/<string:category>")
def category(category):
    if 'uuid' in session:
        logged_in = 'yes'
    else:
        logged_in = 'no'
    all_products = Product.get_products({'category': category})
    category = category.capitalize()
    if category == 'Car_seats':
        category = "Car Seats"
    return render_template("category.html", category=category, all_products=all_products, logged_in=logged_in)

@app.route("/sell")
def sell():
    return render_template("sell.html")

@app.route("/sell/product", methods=['POST'])
def sell_product():
    is_valid = Product.validate_sell_form(request.form)
    if not is_valid:
        return redirect("/sell")

    data = {
        **request.form,
        'id': session['uuid']
    }
    Product.create_product(data)
    return redirect("/account")

@app.route("/sold/<int:id>")
def mark_sold(id):
    Product.mark_sold({'id': id})
    return redirect("/account")

@app.route("/delete/<int:id>")
def delete_product(id):
    Product.delete_product({'id': id})
    return redirect("/account")