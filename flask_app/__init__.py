from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "baby stuff exchange site"

bcrypt = Bcrypt(app)

DATABASE = 'baby_schema'

from flask_app.controllers import controller_users, controller_products