from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Sequence, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from setup_db.database import Base , mapper_registry

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, autoincrement=True ,primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    price = Column(Integer, default=0)

    customer = relationship("Customer", back_populates="reservations", lazy=('selectin'))
    book = relationship("Book", back_populates="reservations", lazy=('selectin'))
