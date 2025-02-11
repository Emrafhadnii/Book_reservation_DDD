from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from src.domain.enums import UserRole
from Reservation import Reservation
from Books import Book
from src.domain.enums import SubscriptionModel


class User(BaseModel):
    id: int
    username: str
    email: str
    user_role: UserRole
    user_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    class Config:
        from_attributes = True
        orm_mode = True

class Customer(BaseModel):
    sub_model: SubscriptionModel
    subscription_end: Optional[datetime] = None
    wallet: int = 0
    reservations: List[Reservation] = []
    user: User


    def __eq__(self, other):
        return isinstance(other, Customer) and self.id == other.id

    @field_validator('wallet')
    def wallet_check(cls, value):
        if value < 0:
            raise ValueError('Wallet cannot be negative')
        return value
    
    class Config:
        from_attributes = True
        orm_mode = True


class Author(BaseModel):
    city_id: int
    goodreads_link: Optional[str] = None
    bank_account: Optional[str] = None
    books: List[Book] = []
    user: User

    def __eq__(self, other):
        return isinstance(other, Author) and self.id == other.id

    class Config:
        from_attributes = True
        orm_mode = True
   


class City(BaseModel):
    id: int
    city_name: str
    authors: List[Author] = []

    def __eq__(self, other):
        return isinstance(other, City) and self.id == other.id

    class Config:
        from_attributes = True
        orm_mode = True


