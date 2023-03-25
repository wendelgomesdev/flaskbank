from flask import Flask
from flask_restful import Api
import os

from config.flask_config import FlaskConfig
from extensions.jwt import jwt
from extensions.sqlalchemy import database

from resources.authentication import Login, Logout, Refresh

from resources.user import UserRegister, UserUpdate, UserDeactivation

from resources.account import Deposit, Transfer, Withdraw, Transactions

def create_app():

    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    jwt.init_app(app)
    database.init_app(app)

    with app.app_context():
        database.create_all()
    
    api = Api(app)
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(Refresh, '/refresh')
    
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserDeactivation, '/deactivation')
    api.add_resource(UserUpdate, '/update')

    api.add_resource(Transfer, '/transfer')
    api.add_resource(Deposit, '/deposit')
    api.add_resource(Withdraw, '/withdraw')
    api.add_resource(Transactions, '/transactions')
    
    return app
