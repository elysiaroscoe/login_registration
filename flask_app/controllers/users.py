from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User #import the Class from models(dot)file

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#####################################


@app.route('/')
def display_form():
    return render_template("index.html")

@app.route('/dashboard')
def display_dashboard():
    return render_template("dashboard.html", user = User.get_by_id({"id": session['user_id']}))



#####################################


@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_registration(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        # "first_name": request.form['first_name'],
        # "last_name": request.form['last_name'],
        # "email": request.form['email'],
        **request.form,
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id #because we are calling the instance of the user object that was just made
    return redirect("/dashboard")


@app.route("/login", methods = ["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_by_email({"email": request.form["email"]})
    session['user_id'] = user.id #because we are calling the instance of the user object that already exists
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")