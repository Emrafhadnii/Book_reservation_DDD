from pydantic import BaseModel,field_validator
from typing import List, Optional
from src.users.domain.entities.Users import Author


class Genre(BaseModel):
    id: int
    gen_name: str

    def __eq__(self, other):
        return isinstance(other, Genre) and self.id == other.id

    class Config:
        from_attributes = True


class Book(BaseModel):
    id: Optional[int]
    title: str
    isbn: str
    price: int
    genre_id: Optional[int]
    units: int
    authors: List[Author] = []
    book_desc: Optional[str] = ""

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
