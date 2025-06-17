from .database import db
from .models import User, Role, Transaction
from flask import current_app as app, jsonify, request, render_template
from flask_security import hash_password, auth_required, roles_required, current_user, login_user, verify_password
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.context import CryptContext

@ app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/api/admin') # admin dashboard
@auth_required('token') # Authentication
@roles_required("admin") # RBAC / Authorization
def admin_home():
    return jsonify ({
        "message" : "Admin logged in successfully"
    })

@app.route('/api/home') # user dashboard
@auth_required('token')
@roles_required('user') 
def user_home():
    user = current_user #current_user fetches the current user from the session 
    return jsonify({
        "username": user.username,
        "email": user.email,
        "password": user.password
    })

@app.route('/api/login', methods=['POST'])
def login(): # Renamed function to 'login' as per your snippet
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(f"Login attempt: email={email}, password={password}")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user = app.security.datastore.find_user(email=email)
    print(f"Found user: {user}")

    if user:
        print(f"Stored password hash: {user.password}")
        is_password_valid = verify_password(password, user.password) # Use verify_password
        print(f"Password verified? {is_password_valid}")

        if is_password_valid:
            login_user(user) # Establish Flask-Login session
            
            # Get user roles and convert them to a list of role names
            user_roles = [role.name for role in user.roles] # user is defined here
            print(f"User roles: {user_roles}") # Debugging print

            # IMPORTANT: Return the expected user data and auth-token for the frontend
            return jsonify({
                "id": user.id,
                "username": user.username,
                "auth-token": user.get_auth_token(),
                "roles": user_roles,
                "message": "Login successful!" # Message for frontend display
            }), 200
        else:
            return jsonify({"message": "Incorrect password"}), 400
    else:
        return jsonify({"message": "User Not Found"}), 404

'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    print("Received POST request to /api/login")
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.data}") 

    body = request.get_json(silent=True)
    
    print(f"Parsed JSON Body: {body}")

    if body is None:
        print("Error: JSON body is None or malformed.")
        return jsonify({"message": "Invalid JSON or missing request body."}), 400

    email = body.get('email')
    password = body.get('password') # This is the plaintext password from the frontend

    print(f"Extracted Email: '{email}'")
    print(f"Extracted Password: '{password}'")

    if not email :
        print("Error: Email is required by backend validation.")
        return jsonify({
            "message" : "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email) 
    
    print(f"Found User: {user}")
    if user:
        print(f"User email: {user.email}")
        stored_password_hash = user.password # Get the hash from the database
        print(f"User stored password hash: {stored_password_hash}")
    else:
        print(f"User not found for email: {email}")
        return jsonify({
                "message" : "User Not Found"
        }), 404

    # Use werkzeug.security.check_password_hash directly
    print("Attempting password verification using werkzeug.security.check_password_hash.")
    is_password_valid = False
    try:
        is_password_valid = check_password_hash(stored_password_hash, password)
        print(f"Werkzeug check_password_hash result: {is_password_valid}")
    except Exception as e:
        print(f"Error during Werkzeug check_password_hash: {e}")

    if is_password_valid:
        print(f"Password verification SUCCESS for user: {user.email}")
        login_user(user) # Establish Flask-Login session (if needed for other auth_required calls)

        # IMPORTANT CHANGE: Return the expected user data and auth-token
        return jsonify({
            "id" : user.id,
            "username" : user.username,
            "auth-token" : user.get_auth_token(), # This is crucial for the frontend
            "message": "Login successful!" # Added message for clarity
        }), 200
    else:
        print(f"Password verification FAILED for user: {user.email}")
        return jsonify({
            "message" : "Incorrect password"
        }), 400
'''

'''
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(f"Login attempt: email={email}, password={password}")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = app.security.datastore.find_user(email=email)
    print(f"Found user: {user}")

    if user:
        print(f"Stored password hash: {user.password}")
        print(f"Password verified? {verify_password(password, user.password)}")

    if user and verify_password(password, user.password):
        # rest of login success code...
        return jsonify({"message": "Logged in!"}), 200

    return jsonify({"message": "login failed pls check your credentials"}), 401
'''
    

'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    print("Received POST request to /api/login")
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.data}") 

    body = request.get_json(silent=True)
    
    print(f"Parsed JSON Body: {body}")

    if body is None:
        print("Error: JSON body is None or malformed.")
        return jsonify({"message": "Invalid JSON or missing request body."}), 400

    email = body.get('email')
    password = body.get('password') # This is the plaintext password from the frontend

    print(f"Extracted Email: '{email}'")
    print(f"Extracted Password: '{password}'")

    if not email :
        print("Error: Email is required by backend validation.")
        return jsonify({
            "message" : "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email) 
    
    print(f"Found User: {user}")
    if user:
        print(f"User email: {user.email}")
        stored_password_hash = user.password # Get the hash from the database
        print(f"User stored password hash: {stored_password_hash}")
    else:
        print(f"User not found for email: {email}")
        return jsonify({
                "message" : "User Not Found"
        }), 404

    # --- TEMPORARY DEBUGGING WITH DIRECT PASSLIB CRYPTCONTEXT ---
    # Create a simple CryptContext that explicitly knows about pbkdf2_sha256
    # This bypasses app.security.pwd_context for a moment to isolate
    # REMOVED: pbkdf2_sha256__salt=app.config.get('SECURITY_PASSWORD_SALT')
    temp_pwd_context = CryptContext(schemes=["pbkdf2_sha256"]) 

    print("Attempting password verification using direct passlib CryptContext.")
    is_password_valid = False
    try:
        is_password_valid = temp_pwd_context.verify(password, stored_password_hash)
        print(f"Direct Passlib verification result: {is_password_valid}")
    except Exception as e:
        print(f"Error during direct Passlib verification: {e}")
        # If there's an error here, it means passlib itself is having trouble with the hash or password.
        # This is a critical diagnostic.

    if is_password_valid:
        print(f"Password verification SUCCESS for user: {user.email}")
        login_user(user) # Establish Flask-Login session (if needed for other auth_required calls)

        return jsonify({
            "id" : user.id,
            "username" : user.username,
            "auth-token" : user.get_auth_token()
        }), 200
    else:
        print(f"Password verification FAILED for user: {user.email}")
        return jsonify({
            "message" : "Incorrect password"
        }), 400
    # --- END TEMPORARY DEBUGGING ---
'''
    
'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    print("Received POST request to /api/login")
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.data}") 

    body = request.get_json(silent=True)
    
    print(f"Parsed JSON Body: {body}")

    if body is None:
        print("Error: JSON body is None or malformed.")
        return jsonify({"message": "Invalid JSON or missing request body."}), 400

    email = body.get('email')
    password = body.get('password') # This is the plaintext password from the frontend

    print(f"Extracted Email: '{email}'")
    print(f"Extracted Password: '{password}'")

    if not email :
        print("Error: Email is required by backend validation.")
        return jsonify({
            "message" : "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email) 
    
    print(f"Found User: {user}")
    if user:
        print(f"User email: {user.email}")
        stored_password_hash = user.password # Get the hash from the database
        print(f"User stored password hash: {stored_password_hash}")
    else:
        print(f"User not found for email: {email}")
        return jsonify({
                "message" : "User Not Found"
        }), 404

    # --- TEMPORARY DEBUGGING WITH DIRECT PASSLIB CRYPTCONTEXT ---
    # Create a simple CryptContext that explicitly knows about pbkdf2_sha256
    # This bypasses app.security.pwd_context for a moment to isolate
    temp_pwd_context = CryptContext(schemes=["pbkdf2_sha256"],
                                    pbkdf2_sha256__salt=app.config.get('SECURITY_PASSWORD_SALT')) # Ensure salt is passed

    print("Attempting password verification using direct passlib CryptContext.")
    is_password_valid = False
    try:
        is_password_valid = temp_pwd_context.verify(password, stored_password_hash)
        print(f"Direct Passlib verification result: {is_password_valid}")
    except Exception as e:
        print(f"Error during direct Passlib verification: {e}")
        # If there's an error here, it means passlib itself is having trouble with the hash or password.
        # This is a critical diagnostic.

    if is_password_valid:
        print(f"Password verification SUCCESS for user: {user.email}")
        login_user(user) # Establish Flask-Login session (if needed for other auth_required calls)

        return jsonify({
            "id" : user.id,
            "username" : user.username,
            "auth-token" : user.get_auth_token()
        }), 200
    else:
        print(f"Password verification FAILED for user: {user.email}")
        return jsonify({
            "message" : "Incorrect password"
        }), 400
    # --- END TEMPORARY DEBUGGING ---
'''

'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    print("Received POST request to /api/login")
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.data}") 

    body = request.get_json(silent=True)
    
    print(f"Parsed JSON Body: {body}")

    if body is None:
        print("Error: JSON body is None or malformed.")
        return jsonify({"message": "Invalid JSON or missing request body."}), 400

    email = body.get('email')
    password = body.get('password') # This is the plaintext password from the frontend

    print(f"Extracted Email: '{email}'")
    print(f"Extracted Password: '{password}'")

    if not email :
        print("Error: Email is required by backend validation.")
        return jsonify({
            "message" : "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email) 
    
    print(f"Found User: {user}")
    if user:
        print(f"User email: {user.email}")
        stored_password_hash = user.password # Get the hash from the database
        print(f"User stored password hash: {stored_password_hash}")
    else:
        print(f"User not found for email: {email}")
        return jsonify({
                "message" : "User Not Found"
        }), 404

    # --- FINAL IMPORTANT CHANGE STARTS HERE ---
    # Use Flask-Security's password context for verification.
    # This is designed to work with your SECURITY_PASSWORD_HASH and SECURITY_PASSWORD_SALT settings.
    print(f"Attempting password verification using app.security.pwd_context.verify.")
    
    if app.security.pwd_context.verify(password, stored_password_hash):
        print(f"Password verification SUCCESS for user: {user.email}")
        # If your frontend is API-token driven, you return the token:
        # If you also want to establish a Flask-Login session, uncomment login_user(user)
        # from flask_security import login_user
        login_user(user) # Establish Flask-Login session (if needed for other auth_required calls)

        return jsonify({
            "id" : user.id,
            "username" : user.username,
            "auth-token" : user.get_auth_token()
        }), 200
    else:
        print(f"Password verification FAILED for user: {user.email}")
        return jsonify({
            "message" : "Incorrect password"
        }), 400
    # --- FINAL IMPORTANT CHANGE ENDS HERE ---
'''


'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    # --- DEBUGGING PRINTS START ---
    print("Received POST request to /api/login")
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.data}") # Raw request body
    # --- DEBUGGING PRINTS END ---

    body = request.get_json(silent=True) # Use silent=True to avoid error if JSON is malformed
    
    # --- DEBUGGING PRINTS START ---
    print(f"Parsed JSON Body: {body}")
    # --- DEBUGGING PRINTS END ---

    if body is None:
        print("Error: JSON body is None or malformed.")
        return jsonify({"message": "Invalid JSON or missing request body."}), 400

    email = body.get('email') # Use .get() to prevent KeyError if key is missing
    password = body.get('password')

    # --- DEBUGGING PRINTS START ---
    print(f"Extracted Email: '{email}'")
    print(f"Extracted Password: '{password}'")
    # --- DEBUGGING PRINTS END ---

    if not email :
        print("Error: Email is required by backend validation.")
        return jsonify({
            "message" : "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email) 
    
    # --- DEBUGGING PRINTS START ---
    print(f"Found User: {user}")
    if user:
        print(f"User email: {user.email}")
        print(f"User stored password hash: {user.password}")
    # --- DEBUGGING PRINTS END ---

    if user :
        # --- DEBUGGING PRINTS START ---
        print(f"Attempting to check password for user: {user.email}")
        print(f"Password provided: '{password}'")
        # --- DEBUGGING PRINTS END ---
        
        if check_password_hash(user.password, password) :
            print(f"Password hash check SUCCESS for user: {user.email}")
            login_user(user) 
            return jsonify({
                "id" : user.id,
                "username" : user.username,
                "auth-token" : user.get_auth_token()
            }), 200
        else:
            print(f"Password hash check FAILED for user: {user.email}")
            return jsonify({
                "message" : "Incorrect password"
            }), 400
    else:
        print(f"User not found for email: {email}")
        return jsonify({
                "message" : "User Not Found"
        }), 404'''

'''
@app.route('/api/login', methods = ['POST'])
def user_login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    if not email :
        return jsonify({
            "message" : "Email is required!"
        }), 400
    user = app.security.datastore.find_user(email=email) # Here find_user is a flask-security method that finds a user based on the attribute I provide(here, email=email)
    if user :
        if check_password_hash(user.password, password) :# Here password refers to the the current password hash generated 
            # if current_user is None:
            login_user(user) # If I don't do this all endpoints that use current_user will fail because there is no information about the current session. This creates the session information
            return jsonify({
                "id" : user.id,
                "username" : user.username,
                "auth-token" : user.get_auth_token()
            }), 200
                #return jsonify({
                #    "message" : "Already logged in !"
                #), 400
        else:
            return jsonify({
                "message" : "Incorrect password"
            }), 400
    else:
        return jsonify({
                "message" : "User Not Found"
        }), 404
'''
        
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

@app.route('/api/pay/<int:trans_id>') # this will be done by GET only so I don't need to specidy which method to use
@auth_required('token') # Authentication
@roles_required("user") # RBAC / Authorization
def payment(trans_id):
    trans = Transaction.query.get()
    # The following line changes the internal status to paid no matter what it's previous tatus was
    trans.internal_status = "paid"
    db.session.commit()
    return jsonify({
        "message" : " Payment Successful !!"
    })

@app.route('/api/delivery/<int:trans_id>', methods = ['POST']) # this will be done by GET only so I don't need to specidy which method to use
@auth_required('token') # Authentication
@roles_required("admin") # RBAC / Authorization
def delivery(trans_id):
    body = request.get_json() # Whatever gets sent will come to our body as a dictionary
    trans = Transaction.query.get()
    trans.delivery_status = body['status']
    db.session.commit()
    return jsonify ({
        "message" : "Delivery status updated!"
    })

@app.route('/api/review/<int:trans_id>', methods = ['POST']) # this will be done by GET only so I don't need to specidy which method to use
@auth_required('token') # Authentication
@roles_required("admin") # RBAC / Authorization
def review(trans_id):
    body = request.get_json() # Whatever gets sent will come to our body as a dictionary ( i.e., the amount and the delivery date)
    trans = Transaction.query.get()
    trans.delivery = body['delivery']
    trans.amount = body['amount']
    trans.internal_status = "pending"
    db.session.commit()
    return{
        "message" : "transaction reviewed"
    }



# IMPORTANT: This catch-all route MUST be placed AFTER all your specific API routes.
# It uses a path converter `<path:path>` to match any path.
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')