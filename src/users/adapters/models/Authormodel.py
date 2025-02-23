from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    goodreads_link = Column(String(200))
    bank_account = Column(String(50))

    books = relationship("Book", secondary="book_author", back_populates="authors", cascade="all, delete")
    user = relationship("User", back_populates="author", uselist=False)
    city = relationship("City", back_populates="authors", uselist=False)
