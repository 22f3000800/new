from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    # required for flask security
    u_id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False) # This is used to create a token. It gives access to particular users 
    active = db.Column(db.Boolean, nullable = False) # Helps in admin control