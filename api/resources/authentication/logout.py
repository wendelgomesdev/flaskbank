from extensions.jwt import get_jwt_identity, get_jwt, user_is_active
from extensions.redis import security_redis
from config.jwt_config import REVOKED_TOKEN_EXPIRES
from flask_restful import Resource

class Logout(Resource):
    @user_is_active()
    def delete(self):
        jti = get_jwt()["jti"]
        security_redis.set(jti, '', ex=REVOKED_TOKEN_EXPIRES)

        current_user = get_jwt_identity()
        security_redis.delete(current_user)
        return {'message': 'Successfully logged out'}, 200