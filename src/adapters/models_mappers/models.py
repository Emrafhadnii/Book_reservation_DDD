from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Sequence, Enum, TIMESTAMP , Sequence
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry
from src.domain.enums import UserRole, SubscriptionModel



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    book_desc = Column(String(100), default='')
    units = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    genre = relationship("Genre", back_populates="books")
    authors = relationship("Author", back_populates="books", secondary="book_author", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="book") 

   

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(13))
    email = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    
    author = relationship("Author", back_populates="user", uselist=False, cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="user", uselist=False, cascade="all, delete-orphan")




class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, Sequence('reservation_id_seq'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    price = Column(Integer, default=0)

    customer = relationship("Customer", back_populates="reservations", cascade="all, delete")
    book = relationship("Book", back_populates="reservations", cascade="all, delete")



class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, Sequence('genre_id_seq'), primary_key=True)
    gen_name = Column(String(50), nullable=False)
    books = relationship("Book", back_populates="genre")




class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    sub_model = Column(Enum(SubscriptionModel), nullable=False)
    subscription_end = Column(TIMESTAMP)
    wallet = Column(Integer, default=0)

    user = relationship("User", back_populates="customer", uselist=False)
    reservations = relationship("Reservation", back_populates="customer", cascade="all, delete")




class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, Sequence('city_id_seq'), primary_key=True)
    city_name = Column(String(50), nullable=False)
    authors = relationship("Author", back_populates="city")




class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    goodreads_link = Column(String(200))
    bank_account = Column(String(50))

    books = relationship("Book", secondary="book_author", back_populates="authors")
    user = relationship("User", back_populates="author", uselist=False)
    city = relationship("City", back_populates="authors", uselist=False)




class BookAuthor(Base):
    __tablename__ = 'book_author'

    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"),primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id',ondelete="CASCADE"), primary_key=True)




def map_models():
    mapper_registry.map_imperatively(Book)
    mapper_registry.map_imperatively(User)
    mapper_registry.map_imperatively(Reservation)
    mapper_registry.map_imperatively(Genre)
    mapper_registry.map_imperatively(Customer)
    mapper_registry.map_imperatively(City)
    mapper_registry.map_imperatively(Author)