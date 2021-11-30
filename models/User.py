from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('role.id'))

    role = relationship('Role')
