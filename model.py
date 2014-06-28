from database import Base, session
from sqlalchemy import Column, Unicode, ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import relationship


class User(Base):
    username = Column(Unicode(128), primary_key=True)
    password = Column(Unicode(128), nullable=False)
    email = Column(Unicode(128), nullable=False)
    first_name = Column(Unicode(128), nullable=False)
    last_name = Column(Unicode(128), nullable=False)
    account_created = Column(DateTime(), nullable=False)
    last_login = Column(DateTime())


