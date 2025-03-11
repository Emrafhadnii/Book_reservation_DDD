from datetime import datetime
from pydantic import BaseModel, field_validator, field_serializer
from src.users.domain.entities.Users import Customer
from src.books.domain.entities.Books import Book
from typing import Optional

class Reservation(BaseModel):
    id: Optional[int] = None
    customer: Customer
    book: Book
    start_time: datetime
    end_time: Optional[datetime]
    price: int

    def __eq__(self, other):
        return isinstance(other, Reservation) and self.id == other.id

    @field_serializer('customer')
    def serialize_customer(self, customer: Customer, _info):
        return customer.model_dump()
    
    @field_serializer('book')
    def serialize_book(self, book: Book, _info):
        return book.model_dump()

    @field_serializer('start_time')
    def serialize_start_time(self, start: datetime, _info):
        return start.isoformat()

    @field_serializer('end_time')
    def serialize_end_time(self, end: Optional[datetime], _info):
        if end is None:
            return None
        return end.isoformat()

    @field_validator('price')
    def price_check(cls, price):
        if price <= 0:
            raise ValueError('Price cannot be negative or zero')
        return price

    class Config:
        from_attributes = True