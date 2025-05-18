from fastapi import FastAPI, HTTPException, Request
from fastapi import Depends
from .session import get_db, engine
from .repository import BookRepository
from sqlalchemy.orm import Session

from .models import Book
from .schemas import BookSchema
import json
import os
app = FastAPI()

BOOKS = 'books.json'


Book.metadata.create_all(bind=engine)




@app.get("/books")
async def get_books(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    
    return repo.get_all()

@app.get("/title/{title}")
async def get_book(title: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    return repo.get_by_title(title)

@app.post("/books", response_model=BookSchema)
async def add_book(book: BookSchema, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    return repo.add(book)

@app.put("/books", response_model=BookSchema)
async def update_book(book: BookSchema, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    return repo.update(book)

@app.delete("/books/{title}")
async def delete_book(title: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    return repo.delete(title)





# @app.get("/books")
# async def get_books():
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
#     return books

# @app.get("/title/{title}")
# async def get_book(title: str):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
#         for book in books:
#             if book['title'] == title:
#                 return book
#         raise  HTTPException(status_code=404, detail="Book not found")
    
# @app.post("/books", response_model=BookSchema)
# async def add_book(book: BookSchema):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     books.append(book.dict())
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return book

# @app.put("/books/{title}", response_model=BookSchema)
# async def update_book(title: str, book: BookSchema):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     for i, b in enumerate(books):
#         if b['title'] == title:
#             books[i] = book.dict()
#             break
#     else:
#         raise  HTTPException(status_code=404, detail="Book not found")
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return book

# @app.delete("/books/{title}")
# async def delete_book(title: str):
#     with open (BOOKS, 'r', encoding='utf-8') as f:
#         books = json.load(f)
    
#     for i, b in enumerate(books):
#         if b['title'] == title:
#             books.pop(i)
#             break
#     else:
#         raise  HTTPException(status_code=404, detail="Book not found")
    
#     with open (BOOKS, 'w', encoding='utf-8') as f:
#         json.dump(books, f, ensure_ascii=False, indent=4)
#     return {"message": "Book deleted"}






