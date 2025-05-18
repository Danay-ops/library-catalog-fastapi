class Book:
    def __init__(self, id, title, author, year, genre, pages, available=True, description=None, cover_url=None):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.pages = pages
        self.available = available
        self.description = description
        self.cover_url = cover_url

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "pages": self.pages,
            "available": self.available,
            "description": self.description,
            "cover_url": self.cover_url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


"""id (уникальный идентификатор)
название
автор
год издания
жанр
количество страниц
доступность (в наличии/выдана)
"""