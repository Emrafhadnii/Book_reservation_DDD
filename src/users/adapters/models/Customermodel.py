from sqlalchemy import Column, Integer, ForeignKey,Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry
from src.users.domain.enums import SubscriptionModel

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    sub_model = Column(Enum(SubscriptionModel), nullable=False)
    subscription_end = Column(TIMESTAMP)
    wallet = Column(Integer, default=0)

    user = relationship("User", back_populates="customer", uselist=False, lazy='selectin')
    reservations = relationship("Reservation", back_populates="customer", cascade="all, delete")
