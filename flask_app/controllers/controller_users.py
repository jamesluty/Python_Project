from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_product import Product


@app.route("/")
def index():
    if 'uuid' in session:
        logged_in = 'yes'
    else:
        logged_in = 'no'
    return render_template("index.html", logged_in=logged_in)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/user", methods=['POST'])
def login_user():
    is_valid = User.validate_login(request.form)
    if not is_valid:
        return redirect('/login')

    return redirect("/")

@app.route("/logout")
def logout():
    User.logout()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/user", methods=['POST'])
def create_user():
    is_valid = User.validate_input(request.form)
    if not is_valid:
        return redirect('/register')

    if not User.validate_email(request.form):
        return redirect('/register')

    phone_number = User.format_password(request.form['phone_number'])

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': pw_hash,
        'phone_number': phone_number
    }

    id = User.create_user(data)

    session['uuid'] = id

    return redirect('/')

@app.route("/account")
def user_account():
    id = session['uuid']
    user = User.get_user({'id': id})
    return render_template("account.html", user=user)