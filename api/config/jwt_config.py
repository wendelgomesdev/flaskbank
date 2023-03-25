import os
from datetime import timedelta

# APP
SECRET_KEY = os.environ.get('SECRET_KEY')
ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
REFRESH_TOKEN_EXPIRES = timedelta(days=30)
REVOKED_TOKEN_EXPIRES = timedelta(days=30)