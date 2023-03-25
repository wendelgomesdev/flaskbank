from flask_restful import Resource, reqparse
from extensions.jwt import get_jwt_identity, user_is_active
from models.account import Account
from models.user import User
from models.transaction import Transaction
from extensions.data_time import get_current_data_time
from extensions.sqlalchemy import database

class Deposit(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('amount', type=float)

    @user_is_active()
    def post(self):
        data = self.arguments.parse_args()
        current_user = get_jwt_identity()

        user = User.query.filter_by(user_id=current_user).first()
        recipient_account = Account.query.filter_by(user_id=user.user_id).first()
        recipient_account.balance += data['amount']
        try:
            database.session.commit()
        except:
            return {'message': 'Error when trying to transfer'}, 500
        
        current_date = get_current_data_time()
        transaction = Transaction(amount=data['amount'], transaction_type='deposit', date=current_date, recipient_account_id=recipient_account.account_id)
        try:
            database.session.add(transaction)
            database.session.commit()
        except:
            return {'message': 'Error registering transfer'}, 500


        return {'message': 'Successful deposit'}, 200