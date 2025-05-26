from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
from application.resources import api
# The following two are like API's created in flask_security
## SQLAlchemyUserDataStore helps us to configure the datastore with the user model and datastore can be used as a function
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import hash_password
def create_app():
    # Create application
    app = Flask(__name__)
    # Import all configurations necessary from config.py
    app.config.from_object(LocalDevelopmentConfig)
    # Connect to database
    db.init_app(app)
    # Connect to restful api
    api.init_app(app)
    # Connect to security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    return app

app = create_app()

# Here we basically create a context of the app.
# This is like telling Flask or VS Code that assume that my app is running , and if it is running do the following. 
with app.app_context():
    db.create_all()
    # This creates a role object
    app.security.datastore.find_or_create_role(name = "admin", description = "Superuser of app")
    # This creates a secondary role object
    app.security.datastore.find_or_create_role(name = "user", description = "General user of app")
    # For these two role objects to get saved in the database
    db.session.commit()

    # Creating admin object
    if not app.security.datastore.find_user(email = "user0@admin.com"):
        app.security.datastore.create_user(email = "user0@admin.com",
                                           username = "admin01",
                                           password = hash_password("1234"),
                                           roles = ['admin'])
    # Creating user object
    if not app.security.datastore.find_user(email = "user1@user.com"):
        app.security.datastore.create_user(email = "user1@user.com", 
                                           username = "user01", 
                                           password = hash_password("1234"), 
                                           roles = ['user'])
    #For these two user objects to be added to the dtabase
    db.session.commit()

from application.routes import *

if __name__ == "__main__":
    app.run()