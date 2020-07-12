from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import  UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db
from blacklist import BLACKLIST

app = Flask(__name__)  #creat a Flask Object
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"]= True  # let WJT to return the error code to app flask
app.config["JWT_BLACKLIST_ENABLED"]= True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"]=['access','refresh']
app.secret_key = 'jose'  # this is for app i can make other for JWT for more secure by app.config['JWT_SECRET_KEY']
api = Api(app)         # Passing the Flask Opject to Api Of flask_restful, so we use falsk-restful the has Flask inside it.

@app.before_first_request
def create_tables():
    db.create_all() # to create tables it will know name and direction from this code 'sqlite:///data.db'

jwt = JWTManager(app)  # it is not creat route with (/auth)

@jwt.user_claims_loader # تعتبر لاحقة للتوكن اقدر اضيف عدة اشياء على الهيدر
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader  #if is in blacklist it will call revoked_token_callback
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader  # is call when token time end
def expired_token_callback():
    return {
        'description': "the token has expired",
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader # this method call when the key is not JWT
def invalid_token_callback(error):
    return {
        'description': "Signature verification failed",
        'error': 'invalid_token'
    }, 401

@jwt.unauthorized_loader # this method call when they don't send us JWT at all
def unauthorized_callback():
    return {
        'description': "Request does not contain an access token",
        'error': 'unauthorized_required'
    }, 401

@jwt.needs_fresh_token_loader # this method call when the fresh token required and they give us a non fresh token
def token_not_fresh_callback():
    return {
        'description': "The token is not fresh",
        'error': 'fresh_token_required'
    }, 401

@jwt.revoked_token_loader # to make log out is a blacklist for a token
def revoked_token_callback():
    return {
        'description': "The tooken has been revoked",
        'error': 'token_revoked'
    }, 401

api.add_resource(Item, "/item/<string:name>")  #define the route for item that call the item class
api.add_resource(ItemList, "/items")         #define the route for items that call the itemlist class
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == '__main__': # to Prevents the app.run from running when we import the file.
    db.init_app(app)
    app.run(port=5000,debug=True)    #run the server on port 5000, and i can use (debug=True) to see if there any problem a clear in text format


