from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from .jsonbin_client import JsonBinClient
from .models import Book
from .schemas import BookSchema
import json
import os


app = FastAPI()





@app.get("/books")
async def get_books(author: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    available: Optional[bool] = None):
    client = JsonBinClient()

    all_books = client.get_books()['record']

    if author:
        all_books = [b for b in all_books if b['author'] == author]

    if genre:
        all_books = [b for b in all_books if b['genre'] == genre]

    if year:
        all_books = [b for b in all_books if b['year'] == year]

    if available:
        all_books = [b for b in all_books if b['available'] == available]

    return all_books


@app.get("/title/{title}")
async def get_book(title: str):
    client = JsonBinClient()
    return client.get_book(title=title)


@app.post("/books", response_model=BookSchema)
async def add_book(book: BookSchema):
    client = JsonBinClient()
    return client.add_book(book.dict())

@app.put("/books", response_model=BookSchema)
async def update_book(book: BookSchema):
    client = JsonBinClient()
    return client.update_book(book.dict())

@app.delete("/books/{id}")
async def delete_book(id: int):
    client = JsonBinClient()
    return client.delete_book(id)


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
