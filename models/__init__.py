import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import (
    POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, 
    POSTGRESQL_DATABASE, POSTGRESQL_PORT
)

# Create sqlalchemy session
username = POSTGRESQL_USER
password = POSTGRESQL_PASSWORD
host = POSTGRESQL_HOST
port = POSTGRESQL_PORT
database = POSTGRESQL_DATABASE
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
