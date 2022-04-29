from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re


class Product:
    def __init__( self , data ):
        self.id = data['id']
        self.url = data['url']
        self.summary = data['summary']
        self.description = data['description']
        self.category = data['category']
        self.price = data['price']
        self.sold = data['sold']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_products(cls, data):
        query = "SELECT * FROM products WHERE category = %(category)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        categories = []

        if results:
            for item in results:
                categories.append(item)

            return categories

        return False

    @classmethod
    def create_product(cls, data):
        query = "INSERT INTO products (url, summary, description, category, price, user_id) VALUES (%(url)s, %(summary)s, %(description)s, %(category)s, %(price)s, %(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def mark_sold(cls, data):
        query = "UPDATE products SET sold = 1 WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_sell_form(form_data):
        is_valid = True
        if len(form_data['summary']) <= 0:
            flash("Summary is required!", 'err_summary')
            is_valid = False

        if len(form_data['description']) <= 0:
            flash("Description is required!", 'err_description')
            is_valid = False

        price = form_data['price'].replace("$", "")
        if len(price) <= 0:
            flash("Price is required!", 'err_price')
            is_valid = False

        return is_valid