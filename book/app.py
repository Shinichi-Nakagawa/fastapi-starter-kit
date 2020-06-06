from datetime import datetime

from sqlalchemy import desc
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, validator

from db import DatabaseSession, Book

api = APIRouter()


# Dependency
def get_db(request: Request):
    return request.state.db


class BookModel(BaseModel):
    title: str

    class Meta:
        min_length = 1
        max_length = 250
        msg_length = f"title.length(min={min_length}, max={max_length})"

    @validator('title')
    def validator_title(cls, v):
        length = len(v)
        if length < cls.Meta.min_length or length > cls.Meta.max_length:
            raise ValueError(f'{cls.Meta.msg_length}: {v}({length})')
        return v


@api.get("/")
async def index(db: DatabaseSession = Depends(get_db)):
    return db.query(Book).order_by(desc(Book.id)).all()


@api.get("/{book_id}")
async def get(book_id: int, db: DatabaseSession = Depends(get_db)):
    return db.query(Book).filter(Book.id == book_id).first()


@api.post("/")
async def create(book: BookModel, db: DatabaseSession = Depends(get_db)):
    now = datetime.now()
    model = Book(title=book.title, created_at=now, read=False)
    db.add(model)
    db.commit()
    return {
        'id': model.id,
        'title': model.title,
        'created_at': model.created_at.isoformat()
    }


@api.put("/{book_id}")
async def update(book_id: int, db: DatabaseSession = Depends(get_db)):
    model = db.query(Book).filter(Book.id == book_id).first()
    model.read = True
    db.add(model)
    db.commit()
    return {
        'id': model.id,
    }


@api.delete("/{book_id}")
async def delete(book_id: int, db: DatabaseSession = Depends(get_db)):
    model = db.query(Book).filter(Book.id == book_id).first()
    db.delete(model)
    db.commit()
    return {
        'id': model.id,
    }
