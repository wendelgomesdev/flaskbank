from flask import abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, create_refresh_token
from extensions.redis import security_redis
from config.jwt_config import REFRESH_TOKEN_EXPIRES
from models.user import User

jwt = JWTManager()

# função para verificar se o token está na blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token_in_redis = security_redis.get(jti)
    if token_in_redis is not None:
        return True

def user_is_active(refresh=False):
    def decorator(function):
        @jwt_required(refresh=refresh)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(user_id=current_user).first()
            if user and user.active:
                return function(*args, **kwargs)
            else:
                abort(401, description='Disabled user, contact support')
        return wrapper
    return decorator

def generate_token(user_identity, fresh):
    access_token = create_access_token(identity=user_identity, fresh=fresh)
    refresh_token = create_refresh_token(identity=user_identity)
    
    # Adiciona o refresh token ao Redis
    security_redis.set(user_identity, refresh_token, ex=REFRESH_TOKEN_EXPIRES)

    return {'access_token': access_token, 'refresh_token': refresh_token}
