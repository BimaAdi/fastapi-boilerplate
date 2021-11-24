import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create sqlalchemy session
if os.environ.get('ENVIRONTMENT') != 'prod':
    from dotenv import load_dotenv
    load_dotenv()

username = os.environ.get('POSTGRESQL_USER')
password = os.environ.get('POSTGRESQL_PASSWORD')
host = os.environ.get('POSTGRESQL_HOST')
port = os.environ.get('POSTGRESQL_PORT')
database = os.environ.get('POSTGRESQL_DATABASE')
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
# To use session for query, insert, update and delete see:
# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker
Session = sessionmaker(engine, future=True)

# base for model
Base = declarative_base()

# for alembic automigrations
from .Role import Role
from .User import User
from .Post import Post
