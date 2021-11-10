# MODELS HOLD THE CLASSES AND METHODS
# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
    # create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument


# model the class after the user table from our database
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return User(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_schema').query_db(query,data)
        #no matching user
        if len(results) == 0:
            return False
        return User(results[0])


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("login_schema").query_db(query, data)
        #this return is equal to the id of the newly created user



#validations as static methods

    @staticmethod
    def validate_registration(user):
        is_valid = True #we assume this is true
        if len(user['first_name']) < 2:
            flash ("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash ("Last name must be at least 2 characters")
            is_valid = False
        if len(user['password']) < 10:
            flash ("Password must be at least 10 characters")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords did not match")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter a valid email")
            is_valid = False
        else:
            usedemail = User.get_by_email({"email": user['email']})
            if usedemail:
                flash("Email in use, please log in")
        return is_valid



    @staticmethod
    def validate_login(form):
        usedemail = User.get_by_email({"email": form['email']})
        
        if not usedemail:
            flash("Invalid credentials")
            return False

        if not bcrypt.check_password_hash(usedemail.password, form["password"]):
            flash("Invalid credentials")
            return False

        return True