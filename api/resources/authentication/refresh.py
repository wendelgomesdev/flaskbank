from extensions.jwt import get_jwt_identity, get_jwt, user_is_active, generate_token
from extensions.redis import security_redis
from config.jwt_config import REVOKED_TOKEN_EXPIRES, REFRESH_TOKEN_EXPIRES
from flask_restful import Resource

class Refresh(Resource):
    @user_is_active(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        security_redis.set(jti, '', ex=REVOKED_TOKEN_EXPIRES)

        current_user = get_jwt_identity()

        # Verificar se o refresh token está presente no banco de dados
        if not security_redis.exists(current_user):
            return 401

        # Retornar os novos tokens para o cliente
        return generate_token(current_user, False), 200