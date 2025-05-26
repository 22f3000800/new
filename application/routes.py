from .database import db
from .models import User, Role
from flask import current_app as app, jsonify, request
from flask_security import hash_password, auth_required, roles_required, current_user

@ app.route('/', methods = ['GET'])
def home():
    return "<h1> This is my home page </h1>"

@app.route('/api/admin') # admin dashboard
@auth_required('token') # Authentication
@roles_required("admin") # RBAC / Authorization
def admin_home():
    return jsonify ({
        "message" : "Admin logged in successfully"
    })

@app.route('/api/home') # user dashboard
@auth_required('token')
@roles_required(['user', 'admin']) # or
def user_home():
    user = current_user #current_user fetches the current user from the session 
    return jsonify({
        "username": user.username,
        "email": user.email,
        "password": user.password
    })

@app.route('/api/register', methods = ['POST']) # this is the  api endpoint which is going to takr data in the form of request body from us and directly store it into the database
def create_user(): # Creating a new user
    credentials = request.get_json() # we take the information from the request body . It will be captured in the form of a dictionary
    if not app.security.datastore.find_user(email = credentials["email"]):
        app.security.datastore.create_user(email = credentials["email"],
                                           username = credentials["username"],
                                           password = hash_password(credentials["password"]),
                                           roles = ['user'])
        db.session.commit()
        return jsonify({
            "messsage" : "User created successfully !!!"
        }), 201
    # else condition - This will run only if the user alreafy exists
    return jsonify({
        "message" : "User already exists!"
    }), 400