from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    AUTHOR = "AUTHOR"

class SubscriptionModel(Enum):
    FREE = "FREE"
    PLUS = "PLUS"
    PREMIUM = "PREMIUM"