from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
