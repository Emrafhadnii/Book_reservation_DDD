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
    price: float

    def __init__(self,id: int,customer: Customer,book: Book,start_time: datetime,end_time: datetime,price: float):
        super().__init__(id=id,customer=customer,book=book,start_time=start_time,end_time=end_time,price=price)

    def __eq__(self, other):
        return isinstance(other, Reservation) and self.id == other.id

    class Config:
        from_attributes = True