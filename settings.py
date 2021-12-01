import os

if os.environ.get('ENVIRONTMENT') != 'prod':
    from dotenv import load_dotenv
    load_dotenv()

POSTGRESQL_USER = os.environ.get('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.environ.get('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = os.environ.get('POSTGRESQL_HOST')
POSTGRESQL_PORT = os.environ.get('POSTGRESQL_PORT')
POSTGRESQL_DATABASE = os.environ.get('POSTGRESQL_DATABASE')

JWT_PREFIX = os.environ.get('JWT_PREFIX', 'Bearer')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
