from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
from application.resources import api
# Re-add hash_password as we will use it explicitly for initial user creation
from flask_security import Security, SQLAlchemyUserDatastore, hash_password 
import uuid


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore, register_blueprint=False)

    
    app.app_context().push()
    return app

app = create_app()

with app.app_context():
    db.create_all()

    # --- DEBUGGING PRINTS FOR FLASK-SECURITY CONFIG START ---
    print("\n--- Flask-Security Configuration Check ---")
    print(f"SECURITY_PASSWORD_HASH from config: {app.config.get('SECURITY_PASSWORD_HASH')}")
    print(f"SECURITY_PASSWORD_SALT from config: {app.config.get('SECURITY_PASSWORD_SALT')}")
    print(f"Flask DEBUG setting: {app.config.get('DEBUG')}")
    
    # This diagnostic check might not work on newer Flask-Security versions, removed for now.
    # try:
    #     current_hasher = app.security.password_manager.pwd_context.current_scheme
    #     print(f"Flask-Security's CURRENT active password hasher: {current_hasher}")
    # except Exception as e:
    #     print(f"Could not determine Flask-Security's current hasher: {e}")
    
    print("--- End Flask-Security Configuration Check ---\n")
    # --- DEBUGGING PRINTS FOR FLASK-SECURITY CONFIG END ---
    
    # Create roles
    admin_role = app.security.datastore.find_or_create_role(name="admin", description="Superuser of app")
    user_role = app.security.datastore.find_or_create_role(name="user", description="General user of app")
    db.session.commit()

    # Create admin user if not exists
    if not app.security.datastore.find_user(email="user0@admin.com"):
        print("Creating admin user...")
        app.security.datastore.create_user(
            email="user0@admin.com",
            username="admin01",
            password=hash_password("1234"),
            roles=[admin_role],   # assign Role object here
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )

    # Create regular user if not exists
    if not app.security.datastore.find_user(email="user1@user.com"):
        print("Creating regular user...")
        app.security.datastore.create_user(
            email="user1@user.com",
            username="user01",
            password=hash_password("1234"),
            roles=[user_role],    # assign Role object here
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )
    '''
    app.security.datastore.find_or_create_role(name = "admin", description = "Superuser of app")
    app.security.datastore.find_or_create_role(name = "user", description = "General user of app")
    db.session.commit()

    # Creating admin object
    if not app.security.datastore.find_user(email = "user0@admin.com"):
        print("Creating admin user...")
        # IMPORTANT CHANGE: Explicitly hash password using Flask-Security's hash_password
        app.security.datastore.create_user(email = "user0@admin.com",
                                           username = "admin01",
                                           password = hash_password("1234"), # <--- CHANGE HERE
                                           roles = ['admin'])
    # Creating user object
    if not app.security.datastore.find_user(email = "user1@user.com"):
        print("Creating regular user...")
        # IMPORTANT CHANGE: Explicitly hash password using Flask-Security's hash_password
        app.security.datastore.create_user(email = "user1@user.com", 
                                           username = "user01", 
                                           password = hash_password("1234"), # <--- CHANGE HERE
                                           roles = ['user'])
    '''
    db.session.commit()

from application.routes import *

if __name__ == "__main__":
    app.run()





'''
from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
from application.resources import api
# The following two are like API's created in flask_security
## SQLAlchemyUserDataStore helps us to configure the datastore with the user model and datastore can be used as a function
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
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
    app.security = Security(app, datastore, register_blueprint=False) # register_blueprint=False prevents Flask-Security from registering its default routes like /login, /register, etc.
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
                                           password = "1234",
                                           roles = ['admin'])
    # Creating user object
    if not app.security.datastore.find_user(email = "user1@user.com"):
        app.security.datastore.create_user(email = "user1@user.com", 
                                           username = "user01", 
                                           password = "1234", 
                                           roles = ['user'])
    #For these two user objects to be added to the dtabase
    db.session.commit()

from application.routes import *

if __name__ == "__main__":
    app.run()

'''