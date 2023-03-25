from models.user import User
from models.account import Account
from flask_restful import Resource, reqparse
from extensions.sqlalchemy import database
from extensions.data_time import get_current_data_time
import random

class UserRegister(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('username', type=str)
        self.arguments.add_argument('email', type=str)
        self.arguments.add_argument('password', type=str)
        self.arguments.add_argument('account_type', type=str)

    def get(self):
        return jsonify(csrf_token=generate_csrf())
    
    def post(self):
        data = self.arguments.parse_args()

        check_availability = User.query.filter_by(username=data['username']).first()
        if check_availability:
            return {'message': f' {data["username"]} already exists!'}
        
        user = User()
        data["password"] = user.generate_password(data["password"])
        
        current_date = get_current_data_time()

        for key, value in data.items():
            if value is not None and key != 'account_type':
                setattr(user, key, value)   
        user.created_at = current_date
        try:
            database.session.add(user)
            database.session.commit()
        except:
            return {'message': 'Error inserting user!'}, 500
        
        account_number = random.randint(100000, 999999)
        account = Account(account_type=data['account_type'], user_id=user.user_id, account_number=account_number, created_at=current_date)
        try:
            database.session.add(account)
            database.session.commit()
        except:
            return {'message': 'Error creating account for user!'}, 500
        
        return {'account number': account_number}, 201