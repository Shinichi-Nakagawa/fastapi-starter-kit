from datetime import datetime

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from db import DatabaseSession, Book

api = APIRouter()


# Dependency
def get_db(request: Request):
    return request.state.db


class BookModel(BaseModel):
    title: str


@api.get("/")
async def index(db: DatabaseSession = Depends(get_db)):
    return db.query(Book).all()


@api.get("/book/{book_id}")
async def get(book_id: int, db: DatabaseSession = Depends(get_db)):
    return db.query(Book).filter(Book.id == book_id).first()


@api.post("/")
async def create(book: BookModel, db: DatabaseSession = Depends(get_db)):
    now = datetime.now()
    model = Book(title=book.title, created_at=now, read=False)
    db.add(model)
    db.commit()
    return model


@api.put("/read/{book_id}")
async def update(book_id: int, db: DatabaseSession = Depends(get_db)):
    model = db.query(Book).filter(Book.id == book_id).first()
    model.read = True
    db.add(model)
    db.commit()
    return model


@api.delete("/{book_id}")
async def delete(book_id: int, db: DatabaseSession = Depends(get_db)):
    model = db.query(Book).filter(Book.id == book_id).first()
    db.delete(model)
    db.commit()
