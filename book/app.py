from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db import session, DatabaseSession, Book

api = APIRouter()


class BookModel(BaseModel):
    title: str


@api.get("/")
async def index(db: DatabaseSession = Depends(session)):
    return db.query(Book).all()


@api.get("/book/{id}")
async def get(id: int, db: DatabaseSession = Depends(session)):
    return db.query(Book).filter(Book.id == id).first()


@api.post("/")
async def create(book: BookModel, db: DatabaseSession = Depends(session)):
    now = datetime.now()
    model = Book(title=book.title, created_at=now, read=False)
    db.add(model)
    db.commit()
    return model


@api.put("/read/{id}")
async def update(id: int, db: DatabaseSession = Depends(session)):
    model = db.query(Book).filter(Book.id == id).first()
    model.read = True
    db.add(model)
    db.commit()
    return model


@api.delete("/{id}")
async def delete(id: int, db: DatabaseSession = Depends(session)):
    model = db.query(Book).filter(Book.id == id).first()
    db.delete(model)
    db.commit()
