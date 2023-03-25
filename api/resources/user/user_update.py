from models.user import User
from models.account import Account
from flask_restful import Resource, reqparse
from extensions.jwt import user_is_active, get_jwt_identity
from extensions.sqlalchemy import database
from extensions.data_time import get_current_data_time

class UserUpdate(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('username', type=str)
        self.arguments.add_argument('email', type=str)
        self.arguments.add_argument('password', type=str, required=True)
        self.arguments.add_argument('new_password', type=str)
        self.arguments.add_argument('account_type', type=str)

    def get(self):
        return jsonify(csrf_token=generate_csrf())
    
    @user_is_active()
    def put(self):
        data = self.arguments.parse_args()
        current_user = get_jwt_identity()

        user = User.query.filter_by(user_id=current_user).first()
        if user:
            
            if user.check_password(data['password']):
                current_date = get_current_data_time()

                for key, value in data.items():
                    validate_fields = value is not None and key != 'account_type' and key != 'new_password' and key != 'password'
                    if validate_fields:
                        setattr(user, key, value) 
                user.modified_at = current_date
                
                if data["new_password"] is not None:
                    user.password = user.generate_password(data["new_password"])

                user_account = Account.query.filter_by(user_id=user.user_id).first()
                user_account.account_type = data['account_type']
                user_account.modified_at = current_date

                try:
                    database.session.commit()
                except:
                    return {'message': 'Error updating user!'}, 500
                
                return {'message': 'successfully saved edits'}, 200
            
            else:
                return {'message': 'Invalid password'}, 401