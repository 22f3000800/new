# This is where we create our RESTFUL api

from flask_restful import Api, Resource, recparse
from .models import *
from flask_security import current_user, auth_required, roles_required, roles_accepted

api = Api()

def roles_list(roles):
    role_list = []
    for role in roles:
        role_list.append(role.name)
    return role_list

parser = recparse.RequestParser()

parser.add_argument('name')
parser.add_argument('type')
parser.add_argument('date')
parser.add_argument('source')
parser.add_argument('destination')
parser.add_argument('description')



class TransApi(Resource):
    @auth_required('token')
    @roles_accepted('user', 'admin') # Here either the user or the admin can access it 
    def get(self):
        transaction = [] # Stores List of transaction objects
        trans_json = [] # Stores list of transaction dictionaries
        if 'admin' in roles_list(current_user.roles):
            transactions = Transaction.query.all()
        else:
            transactions = current_user.trans
        for transaction in transactions:
            this_trans = {} # new empty dictionary
            this_trans["id"] = transaction.id # creating a key:value pair of the dictionary. Here "id" is the key and "transaction.id " is the value
            this_trans["name"] = transaction.name
            this_trans["type"] = transaction.type
            this_trans["date"] = transaction.date
            this_trans["delivery"] = transaction.delivery
            this_trans["source"] = transaction.source
            this_trans["destination"] = transaction.destination
            this_trans["internal_status"] = transaction.internal_status
            this_trans["delivery_status"] = transaction.delivery_status
            this_trans["description"] = transaction.description
            this_trans["user"] = transaction.bearer.username # I can also use current_user.id as both refer to the same 
            this_trans["amount"] = transaction.amount
            trans_json.append(this_trans)

            if trans_json:
                return trans_json
            else:
                return{
                    "message" : "No transactions found"
                }, 404
            
    @auth_required('token')
    @roles_required('user')
    def post(self):
        args = parser.parser_args() # everything provided in the request body comes here in the form of a dictionary
        try:
            # Create transaction object
            transaction = Transaction(name = args['name'],
                                    type = args['type'],
                                    date = args['date'],
                                    source = args['source'],
                                    destination = args['destination'],
                                    description = args['description'],
                                    user_id = current_user.id)
            db.session.add(transaction)
            db.session.commit()
            return {
                "message" : "Transaction created successfully !!!"
            }
        except:
            return {
                "message" : " One or more required fields are missing"
            }, 400

api.add_resource(TransApi, '/api/get','/api/create')