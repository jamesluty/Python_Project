from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)

from flask_app.controllers import controller_users, controller_products