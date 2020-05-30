from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DB_URI = 'sqlite:///./books.db'

engine = create_engine(DB_URI, connect_args={"check_same_thread": False}, echo=True)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(100), unique=True)
    created_at = Column('created_at', Date)
    read = Column('read', Boolean, default=False)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session():
    """
    Get Database Session
    :return:
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class DatabaseSession(Session):
    pass
