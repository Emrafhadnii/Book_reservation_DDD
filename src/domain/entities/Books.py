from pydantic import BaseModel,field_validator
from typing import List, Optional
from Users import Author, User, Book


class Genre(BaseModel):
    id: int
    gen_name: str
    books: List[Book] = []

    def __init__(self,id: int,gen_name: str,books: List[Book] = []):
        super().__init__(id=id,gen_name=gen_name,books=books)

    def __eq__(self, other):
        return isinstance(other, Genre) and self.id == other.id

    class Config:
        from_attributes = True


class Book(BaseModel):
    id: int
    title: str
    isbn: str
    price: float
    genre_id: int
    units: int
    authors: List[Author] = []
    book_desc: Optional[str] = ""

    def __init__(self,id: int,title: str,isbn: str,price: float,genre_id: int,units: int,
                authors: List[Author] = [],book_desc: Optional[str] = ""):
        super().__init__(id=id,title=title,isbn=isbn,price=price,genre_id=genre_id,units=units,
                        authors=authors,book_desc=book_desc)

    def __eq__(self, other):
        return isinstance(other, Book) and self.id == other.id

    @field_validator('price')
    def price_check(cls, value):
        if value <= 0:
            raise ValueError('This book cannot be free')
        return value
    @field_validator('units')
    def unit_check(cls, count):
        if count < 0:
            raise ValueError('The number of books cannot be negative')
        return count
    class Config:
        from_attributes = True