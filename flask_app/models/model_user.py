from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
from flask_app.models import model_product
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.products = []

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, phone_number, street, city, state, zip_code, email, password) VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(street)s, %(city)s, %(state)s, %(zip_code)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            user = cls(results[0])
            return user

        return False

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            user = cls(results[0])
            return user
        
        return False

    @classmethod
    def get_all_selling(cls, data):
        query = "SELECT * FROM users LEFT JOIN products ON users.id = products.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(results[0])

        if results:
            for item in results:
                product_data = {
                    'id': item['products.id'],
                    'url': item['url'],
                    'summary': item['summary'],
                    'description': item['description'],
                    'category': item['category'],
                    'price': item['price'],
                    'sold': item['sold'],
                    'created_at': item['products.created_at'],
                    'updated_at': item['products.updated_at'],
                    'user_id': item['user_id']
                }
                temp_product = model_product.Product(product_data)
                user.products.append(temp_product)
            return user

        return False


    @staticmethod
    def logout():
        return session.clear()

    @staticmethod
    def validate_login(form_data):
        is_valid = True
        if len(form_data['email']) <= 0:
            flash("Email must be included!", 'err_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address!", "err_email_login")
            is_valid = False

        if len(form_data['password']) <= 8:
            flash("Password must be at least 8 characters!", 'err_password_login')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            if potential_user:
                if not bcrypt.check_password_hash(potential_user.password, form_data['password']):
                    flash("Invalid credentials!", 'err_password_login')
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id
            else:
                flash("Invalid credentials!", 'err_password_login')
                is_valid = False

        return is_valid

    @staticmethod
    def validate_input(form_data):
        is_valid = True

        if len(form_data['first_name']) <= 0:
            flash("First name is required!", 'err_first_name')
            is_valid = False

        if len(form_data['last_name']) <= 0:
            flash("Last name is required!", 'err_last_name')
            is_valid = False

        phone_number = form_data['phone_number'].replace("(", "").replace(")", "").replace("-", "")
        if len(phone_number) != 10:
            flash("Must be 10 numbers!", 'err_phone_number')
            is_valid = False

        if len(form_data['street']) <= 0:
            flash("Street is required!", 'err_street')
            is_valid = False

        if len(form_data['city']) <= 0:
            flash("City is required!", 'err_city')
            is_valid = False

        if len(form_data['state']) <= 0:
            flash("State is required!", 'err_state')
            is_valid = False

        if len(form_data['zip_code']) != 5:
            flash("Zip code is required!", 'err_zip_code')
            is_valid = False

        if len(form_data['email']) <= 0:
            flash("Email is required!", 'err_email')
            is_valid = False

        if len(form_data['password']) <= 8:
            flash("Password must be at least 8 characters!", 'err_password')
            is_valid = False

        if len(form_data['confirm_password']) <= 8:
            flash("Password must be at least 8 characters!", 'err_confirm_password')
            is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords must be the same!", 'err_confirm_password')
            is_valid = False

        return is_valid

    @staticmethod
    def format_password(pn):
        phone_number = pn.replace("(", "").replace(")", "").replace("-", "")
        return phone_number

    @staticmethod
    def validate_email(data):
        query = "SELECT * FROM users"
        results = connectToMySQL(DATABASE).query_db(query)
        is_valid = True

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "err_email")
            is_valid = False

        emails = []

        for item in results:
            emails.append(item['email'])

        for email in emails:
            if data['email'] == email:
                flash("Email has already been used", "err_email")
                is_valid = False
                break

        return is_valid