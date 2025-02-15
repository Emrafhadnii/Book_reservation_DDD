from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, delete
from src.domain.repositories.BookABS import BookRepository
from src.adapters.repositories.ReservationRepo import SqlAlchemyReservationRepository
from src.adapters.repositories.CustomerRepo import SqlAlchemyCustomerRepository
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository
from src.domain.entities.Books import Book as BookEntity
from src.domain.entities.Reservations import Reservation as ReservationEntity
from src.domain.entities.Users import Customer as CustomerEntity
from src.adapters.models_mappers.Customermapper import Customermapper
from src.adapters.models_mappers.models import Book as BookSQL
from typing import Optional, List
from src.adapters.models_mappers.Bookmapper import Bookmapper
from datetime import datetime, UTC, timedelta


class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, book: BookEntity) -> None:
        bookSQL = Bookmapper.to_SQL(book)
        self.db.add(bookSQL)
    
    async def update(self, book : BookEntity) -> None:
        bookSQL = Bookmapper.to_SQL(book)
        await self.db.merge(bookSQL)
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        book_to_delete = result.scalar_one_or_none()
        if book_to_delete:
            await self.db.delete(book_to_delete)
    
    async def get_by_id(self, id: int) -> Optional[BookEntity]:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        book = result.scalar_one_or_none()
        return BookEntity.model_validate(book) if book else None
    
    async def get_all(self) -> List[BookEntity]:
        result = await self.db.execute(select(BookSQL))
        books_list = result.scalars().all()
        return list(map(BookEntity.model_validate,books_list))
    
    async def stock_update(self, id, new_stock) -> None:
        result = await self.db.execute(
            select(BookSQL).filter(BookSQL.id == id).options(selectinload(BookSQL.authors)))
        book = result.scalar_one_or_none()
        if book:
            bookentity = BookEntity.model_validate(book)
            bookentity.units += new_stock
            await self.update(bookentity)