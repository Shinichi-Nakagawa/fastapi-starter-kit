import pytest

from typing import Any, Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from book.app import get_db


@pytest.fixture
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


def test_create_book(
        app: FastAPI,
        db_session: Session,
        client: TestClient
):
    response = client.post("/book/", json={"title": "hogefuga"})
    assert response.status_code == 200
