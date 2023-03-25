from flask_restful import Resource, reqparse
from extensions.jwt import user_is_active, get_jwt_identity
from models.account import Account
from models.user import User
from models.transaction import Transaction

class Transactions(Resource):
    
    @user_is_active()
    def get(self):
        current_user = get_jwt_identity()

        user_data = User.query.filter_by(user_id=current_user).first()
        user_account = Account.query.filter_by(user_id=user_data.user_id).first()
        if user_account:
            user_transactions = Transaction.query.filter((Transaction.source_account_id == user_account.account_id) | (Transaction.recipient_account_id == user_account.account_id)).all()
            if user_transactions:
                transactions = []
                for transaction in user_transactions:
                    transaction_date = transaction.date.strftime('%Y-%m-%d %H:%M:%S')
                    transactions.append(
                        {'amount': transaction.amount,
                        'transaction_type': transaction.transaction_type,
                        'date': transaction_date,
                        'source_account_id': transaction.source_account_id,
                        'recipient_account_id': transaction.recipient_account_id
                    })
            else:
                return {'message': 'No transaction found'}, 404
            
            return {'transactions': transactions}, 200