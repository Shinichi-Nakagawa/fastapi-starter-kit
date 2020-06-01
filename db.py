from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

CONNECT_ARGS = {"check_same_thread": False}


def get_engine(uri='sqlite:///./books.db', connect_args=CONNECT_ARGS, echo=True):
    return create_engine(uri, connect_args=connect_args, echo=echo)


Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(100), unique=True)
    created_at = Column('created_at', Date)
    read = Column('read', Boolean, default=False)


engine = get_engine()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session():
    """
    Get Database Session
    :return:
    """
    return SessionLocal()


class DatabaseSession(Session):
    pass
