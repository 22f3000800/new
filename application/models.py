from .database import db
from flask_security import UserMixin, RoleMixin

# Association table for many-to-many relationship between users and roles
users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    # Use association table here
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))
    trans = db.relationship('Transaction', backref='bearer')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # transaction name
    type = db.Column(db.String, nullable=False)  # type of transaction
    date = db.Column(db.String, nullable=False)  # booking date
    delivery = db.Column(db.String, default='to be updated', nullable=False)  # delivery date
    source = db.Column(db.String, nullable=False)  # package source
    destination = db.Column(db.String, nullable=False)  # package destination
    internal_status = db.Column(db.String, default='requested', nullable=False)
    delivery_status = db.Column(db.String, default='in process', nullable=False)
    description = db.Column(db.String)
    amount = db.Column(db.Integer, default=1000)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreign key to User



'''
from .database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    # required for flask security
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False) # This is used to create a token. It gives access to particular users 
    active = db.Column(db.Boolean, nullable = False) # Helps in admin control
    # many-to-many relationship between user and roles
    roles = db.relationship('Role', backref = 'bearer', secondary = 'users_roles') # Here secondary = users_roles  refers to where exactly my association is stored
    # one-to-many relationship between user and transactions
    trans = db.relationship('Transaction', backref = db.backref('users'))
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String)

class UsersRoles(db.Model): # This is a many-to-many relationship
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    
class City(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String, nullable = False) # transaction name
    type = db.Column(db.String, nullable = False) # type of transaction
    date = db.Column(db.String, nullable = False) # this is the date of booking
    delivery = db.Column(db.String,default = 'to be updated', nullable = False) # this is the delivery date
    source = db.Column(db.String, nullable = False) # from where the package is going
    destination = db.Column(db.String, nullable = False) # the destination of the package
    internal_status = db.Column(db.String,default = 'requested', nullable = False)
    delivery_status = db.Column(db.String,default = 'in process', nullable = False)
    description = db.Column(db.String)
    amount = db.Column(db.Integer,default = 1000)
    # one-to-many relationship between user and Transaction
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
'''