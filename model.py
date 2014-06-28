from database import Base
from sqlalchemy import Column, Unicode, ForeignKey, DateTime, Integer, Enum


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(128), nullable=False)
    password = Column(Unicode(128), nullable=False)
    email = Column(Unicode(128), nullable=False)
    first_name = Column(Unicode(128), nullable=False)
    last_name = Column(Unicode(128), nullable=False)
    account_created = Column(DateTime(), nullable=False)
    last_login = Column(DateTime)
    account_type = Column(Enum('publisher', 'advertiser'), nullable=False)


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, ForeignKey('User.id'), primary_key=True)
