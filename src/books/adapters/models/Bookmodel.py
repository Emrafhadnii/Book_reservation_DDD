from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Sequence, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer,autoincrement=True ,primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    book_desc = Column(String(100), default='')
    units = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    authors = relationship("Author", back_populates="books", secondary="book_author", lazy=('selectin'))
    reservations = relationship("Reservation", back_populates="book", cascade="all, delete")
