from models.user import User
from werkzeug.security import check_password_hash
from flask_restful import Resource, reqparse
from extensions.jwt import generate_token

class Login(Resource):
    def __init__(self):
        self.arguments = reqparse.RequestParser()
        self.arguments.add_argument('username', type=str, required=True)
        self.arguments.add_argument('password', type=str, required=True)
    
    def get(self):
        return jsonify(csrf_token='generate_csrf()')
    
    def post(self):
        data = self.arguments.parse_args()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_user_satus():
                check_password = check_password_hash(user.password, password)

                if user and check_password:
                    # Retorna o token para o cliente
                    return generate_token(user.user_id, True), 200
                
                else:
                    return {'message': 'Invalid username or password'}, 401
            else:
                return {'message': 'Disabled user, contact support'}, 401
        else:
            return {'message': 'Invalid username or password'}, 401
        
        

        
        
