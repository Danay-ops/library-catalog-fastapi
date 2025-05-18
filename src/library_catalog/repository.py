from sqlalchemy.orm import Session
from .models import Book
from .schemas import BookSchema


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Book).all()
    
    def get_by_title(self, title: str):
        return self.db.query(Book).filter(Book.title == title).first()
    
    def add(self, book: BookSchema):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def update(self, book: BookSchema):
        db_book = self.get_by_title(book.title)
        db_book.title = book.title
        db_book.author = book.author
        db_book.year = book.year
        db_book.genre = book.genre
        db_book.pages = book.pages
        db_book.available = book.available
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, title: str):
        db_book = self.get_by_title(title)
        self.db.delete(db_book)
        self.db.commit()