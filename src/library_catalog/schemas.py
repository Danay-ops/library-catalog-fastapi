from pydantic import BaseModel

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool = True
