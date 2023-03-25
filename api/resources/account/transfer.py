from flask_restful import Resource, reqparse
from extensions.jwt import user_is_active, get_jwt_identity
from models.account import Account
from models.user import User
from models.transaction import Transaction
from extensions.sqlalchemy import database
from extensions.data_time import get_current_data_time

class Transfer(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('amount', type=float)
        self.arguments.add_argument('account_number', type=str)
        self.arguments.add_argument('password', type=str, required=True)

    @user_is_active()
    def post(self):
        data = self.arguments.parse_args()
        current_user = get_jwt_identity()

        user = User.query.filter_by(user_id=current_user).first()
        user_account = Account.query.filter_by(user_id=user.user_id).first()
        check_balance = user_account.balance < data['amount']
        if check_balance:
            return {'message': 'Insufficient funds'}, 403
        else:
            if user.check_password(data['password']):
                amount = data['amount']
                recipient_account = Account.query.filter_by(account_number=data['account_number']).first()
                if recipient_account:
                    recipient_account.balance += amount
                    user_account.balance -= amount
                    try:
                        database.session.commit()
                    except:
                        return {'message': 'Error when trying to transfer'}, 500
                    
                    current_date = get_current_data_time()
                    transaction = Transaction(amount=data['amount'], transaction_type='transfer', date=current_date, source_account_id=user_account.account_id, recipient_account_id=recipient_account.account_id)
                    try:
                        database.session.add(transaction)
                        database.session.commit()
                    except:
                        return {'message': 'Error registering transfer'}, 500

                    return {'message': f'Successful transfer'}, 200
                
                else:
                    return {'message': 'Invalid account'}, 400