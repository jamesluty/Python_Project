from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re


class Product:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
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