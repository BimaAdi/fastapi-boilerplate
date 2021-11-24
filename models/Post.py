from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models import Base

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    post = Column(Text)
    created_by_id = Column(Integer, ForeignKey('user.id'))

    created_by = relationship('User')
