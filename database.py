from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

mysql_url = URL(drivername='mysql+mysqlconnector', host='localhost',
                database='adbitise', username='adbitise',
                password='oeNung0j')

engine = create_engine(mysql_url)

session = scoped_session(sessionmaker(engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    Base.metadata.create_all(engine)
