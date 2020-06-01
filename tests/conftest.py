from typing import Any, Generator

import pytest

from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

from app import app as test_app

from db import Base, get_engine

engine = get_engine(uri='sqlite:///:memory:')

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(bind=engine)
    _app = test_app
    _app.debug = True
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    session = Session(bind=connection)
    yield session
    session.close()
    connection.close()

