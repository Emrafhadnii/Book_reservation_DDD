from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry
from src.users.domain.enums import UserRole

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(13), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    
    author = relationship("Author", back_populates="user", uselist=False, cascade="all, delete")
    customer = relationship("Customer", back_populates="user", uselist=False, cascade="all, delete")
