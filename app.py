from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
# The following two are like API's created in flask_security
## SQLAlchemyUserDataStore helps us to configure the datastore with the user model and datastore can be used as a function
from flask_security import Security, SQLAlchemyUserDatastore

def create_app():
    # Create application
    app = Flask(__name__)
    # Import all configurations necessary from config.py
    app.config.from_object(LocalDevelopmentConfig)
    # Connect to database
    db.init_app(app)
    # Connect to security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    return app

app = create_app()

if __name__ == "__main__":
    app.run()