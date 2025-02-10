from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    AUTHOR = "author"

class SubscriptionModel(Enum):
    FREE = "free"
    PLUS = "plus"
    PREMIUM = "premium"

class ReservationStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    QUEUED = "queued"
