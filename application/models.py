from .database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    # required for flask security
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False) # This is used to create a token. It gives access to particular users 
    active = db.Column(db.Boolean, nullable = False) # Helps in admin control
    roles = db.relationship("Role", backref = 'bearer', secondary = "")

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String)

class UserRole(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user_id'))
    role_id = db.Column(db.Integer,db.ForeignKey('role_id'))