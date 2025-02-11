from datetime import datetime
from pydantic import BaseModel, field_validator
from Users import Customer
from Books import Book


class Reservation(BaseModel):
    id: int
    customer: Customer
    book: Book
    start_time: datetime
    end_time: datetime
    price: int

    def __eq__(self, other):
        return isinstance(other, Reservation) and self.id == other.id

    @field_validator('price')
    def price_check(cls, price):
        if price <= 0:
            raise ValueError('Price cannot be negative or zero')
        return price

    class Config:
        from_attributes = True
        orm_mode = True