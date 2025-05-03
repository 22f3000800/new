# We are creating configurations , these help us link our flask application with various other extentions
class Config():
    # Variables created 
    DEGUB = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class LocalDevelopmentConfig(Config):
    # Configurations for database
    SQLALCHEMY_DATABASE_URI = "sqlite:///new.sqlite3"
    DEBUG = True

    # Configuration for security
    SECRET_KEY = "this-is-a-secretkey" # This helps us to encrypt the user credentials in the session
    SECURITY_PASSWORD_HASH = "bcrypt"  # This stores the mechanism I'm going to use (here bcrypt). This is a mechanism for hashing password
    SECURITY_PASSWORD_SALT = "this-is-a-password-salt" # It is similar to SECRET_KEY but it helps in encrypting(hashing) the password
    WTF_CSRF_ENABLED = False 
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token" # It is related to the form . this is to make sure that the data coming from the form is actually coming from a form of the same application and not from another random application.
    