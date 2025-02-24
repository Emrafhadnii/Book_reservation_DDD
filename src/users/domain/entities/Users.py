from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from src.users.domain.enums import UserRole
from src.users.domain.enums import SubscriptionModel


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    user_role: str
    user_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    class Config:
        from_attributes = True

class Customer(BaseModel):
    sub_model: str = "FREE"
    subscription_end: Optional[datetime] = None
    wallet: int = 0
    user: Optional[User]

    def __eq__(self, other):
        return isinstance(other, Customer) and self.user.id == other.user.id

    @field_validator('wallet')
    def wallet_check(cls, value):
        if value < 0:
            raise ValueError('Wallet cannot be negative')
        return value
    
    class Config:
        from_attributes = True

class Author(BaseModel):
    city_id: int
    goodreads_link: Optional[str] = None
    bank_account: Optional[str] = None
    user: User

    def __eq__(self, other):
        return isinstance(other, Author) and self.user.id == other.user.id

    class Config:
        from_attributes = True
   


class City(BaseModel):
    id: int
    city_name: str
    authors: List[Author] = []

    def __eq__(self, other):
        return isinstance(other, City) and self.id == other.id

    class Config:
        from_attributes = True


class charge_account_model(BaseModel):
    id: int
    amount: int

    @field_validator('amount')
    def wallet_check(cls, value):
        if value < 0:
            raise ValueError('charge amount cannot be negative')
        return value
class purchase_model(BaseModel):
    id: int
    sub_model: str

    @field_validator('sub_model')
    def wallet_check(cls, value):
        if value not in ("PLUS","PREMIUM"):
            raise ValueError('sub_model is invalid')
        return value