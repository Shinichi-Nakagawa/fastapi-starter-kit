from datetime import datetime

import pytest

from typing import Any, Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from book.app import get_db, BookModel
from db import Book


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
    now = datetime.now()
    response = client.post("/book/", json={"title": "money ball"})
    assert response.status_code == 200
    body = response.json()
    assert body['id'] == 1
    assert body['title'] == "money ball"
    assert body['created_at'] == now.strftime('%Y-%m-%d')

    book = db_session.query(Book).get(1)
    assert book.id == 1
    assert book.title == "money ball"
    assert book.created_at.isoformat() == now.strftime('%Y-%m-%d')
    assert not book.read


def test_update_book(
        app: FastAPI,
        db_session: Session,
        client: TestClient
):
    response_base_data = client.post("/book/", json={"title": "big data baseball"})
    body = response_base_data.json()
    book = db_session.query(Book).get(body.get('id'))
    assert not book.read
    response = client.put(f"/book/{body.get('id')}")
    assert response.status_code == 200
    body = response.json()
    book = db_session.query(Book).get(body.get('id'))
    assert book.read


def test_delete_book(
        app: FastAPI,
        db_session: Session,
        client: TestClient
):
    response_base_data = client.post("/book/", json={"title": "astro ball"})
    body = response_base_data.json()
    book = db_session.query(Book).get(body.get('id'))
    assert not book.read
    response = client.delete(f"/book/{body.get('id')}")
    assert response.status_code == 200
    body = response.json()
    book = db_session.query(Book).get(body.get('id'))
    assert not book


def test_get_book(
        app: FastAPI,
        db_session: Session,
        client: TestClient
):
    now = datetime.now()
    client.post("/book/", json={"title": "野村ノート"})
    client.post("/book/", json={"title": "野村の教え"})
    client.post("/book/", json={"title": "感情をコントロールする技術"})
    response = client.get(f"/book/1")
    body = response.json()
    assert body['id'] == 1
    assert body['title'] == "野村ノート"
    assert body['created_at'] == now.strftime('%Y-%m-%d')


def test_get_index(
        app: FastAPI,
        db_session: Session,
        client: TestClient
):
    now = datetime.now()
    _ = client.post("/book/", json={"title": "アルゴリズム図鑑"})
    _ = client.post("/book/", json={"title": "機械学習図鑑"})
    _ = client.post("/book/", json={"title": "機械学習のための特徴量エンジニアリング"})
    response = client.get("/book/")
    body = response.json()
    assert len(body) == 3
    assert body[0]['id'] == 3
    assert body[0]['title'] == '機械学習のための特徴量エンジニアリング'
    assert body[0]['created_at'] == now.strftime('%Y-%m-%d')
    assert body[1]['id'] == 2
    assert body[1]['title'] == '機械学習図鑑'
    assert body[1]['created_at'] == now.strftime('%Y-%m-%d')
    assert body[2]['id'] == 1
    assert body[2]['title'] == 'アルゴリズム図鑑'
    assert body[2]['created_at'] == now.strftime('%Y-%m-%d')


def test_book_model():
    book = BookModel(title='Money Ball')
    assert book.title == 'Money Ball'
    book = BookModel(title='bigdata baseball')


def test_book_model_value_error():
    with pytest.raises(ValueError):
        BookModel(title='')
    with pytest.raises(ValueError):
        long_title = "".join(['a' for _ in range(251)])
        BookModel(title=long_title)
