from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry
from src.users.domain.enums import UserRole, SubscriptionModel


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, autoincrement=True ,primary_key=True)
    city_name = Column(String(50), nullable=False)
    authors = relationship("Author", back_populates="city")