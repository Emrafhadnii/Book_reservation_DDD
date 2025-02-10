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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

    def __init__(self,id: int,username: str,email: str,user_role: UserRole,
                first_name: Optional[str] = None,last_name: Optional[str] = None,
                phone: Optional[str] = None):
        super().__init__(id=id,username=username,email=email,user_role=user_role,
                        first_name=first_name,last_name=last_name,phone=phone)
    
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    class Config:
        from_attributes = True

class Customer(User):
    sub_model: SubscriptionModel
    subscription_end: Optional[datetime] = None
    wallet: int = 0
    reservations: List[Reservation] = []

    def __init__(self,id: int,username: str,email: str,user_role: UserRole,
                sub_model: SubscriptionModel,subscription_end: Optional[datetime] = None,
                wallet: int = 0,reservations: List[Reservation] = [],**kwargs):
        super().__init__(id=id,username=username,email=email,user_role=user_role,**kwargs)
        self.sub_model = sub_model
        self.subscription_end = subscription_end
        self.wallet = wallet
        self.reservations = reservations

    @field_validator('wallet')
    def wallet_check(cls, value):
        if value < 0:
            raise ValueError('Wallet cannot be negative.')
        return value


class Author(User):
    city_id: int
    goodreads_link: Optional[str] = None
    bank_account: Optional[str] = None
    books: List[Book] = []

    def __init__(self,id: int,username: str,email: str,user_role: UserRole,city_id: int,
        goodreads_link: Optional[str] = None,bank_account: Optional[str] = None,
        books: List[Book] = [],**kwargs):
        
        super().__init__(id=id,username=username,email=email,user_role=user_role,**kwargs)
        self.city_id = city_id
        self.goodreads_link = goodreads_link
        self.bank_account = bank_account
        self.books = books


class City(BaseModel):
    id: int
    city_name: str
    city_detail: Optional[str] = None
    authors: List[Author] = []

    def __init__(self,id: int,city_name: str,city_detail: Optional[str] = None,authors: List[Author] = []):
        super().__init__(id=id,city_name=city_name,city_detail=city_detail,authors=authors)

    def __eq__(self, other):
        return isinstance(other, City) and self.id == other.id

    class Config:
        from_attributes = True


