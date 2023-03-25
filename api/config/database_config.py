import os

# DATABASE
DATABASE_USER = os.environ.get('POSTGRES_USER')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DATABASE_HOST = os.environ.get('HOST')
DATABASE_PORT = os.environ.get('PORT')
DATABASE_NAME = os.environ.get('POSTGRES_DB')