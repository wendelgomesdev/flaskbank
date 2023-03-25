from models.user import User
from models.account import Account
from flask_restful import Resource, reqparse
from extensions.jwt import user_is_active, get_jwt_identity
from werkzeug.security import check_password_hash
from extensions.sqlalchemy import database

class UserDeactivation(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('password', type=str, required=True)

    def get(self):
        return jsonify(csrf_token=generate_csrf())
    
    @user_is_active()
    def delete(self):
        data = self.arguments.parse_args()

        current_user = get_jwt_identity()

        user = User.query.filter_by(user_id=current_user).first()
        user_account = Account.query.filter_by(user_id=user.user_id).first()
        if user:
            check_password = check_password_hash(user.password, data['password'])
            if check_password:
                
                check_user_status = user.active or user_account.active
                if check_user_status:
                    user.active = False
                    user_account.active = False

                try:
                    database.session.commit()
                except:
                    return {'message': 'Error deactivating user!'}, 500