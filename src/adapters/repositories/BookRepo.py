from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.BookABS import BookRepository
from src.domain.entities.Books import Book as BookEntity
from src.adapters.models_mappers.models import Book as BookSQL
from typing import Optional, List
from src.adapters.models_mappers.Bookmapper import Bookmapper
from setup_db.database import asyncsession

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: AsyncSession = asyncsession):
        self.db = db

    async def add(self, book: BookEntity) -> None:
        bookSQL = Bookmapper.to_SQL(book)
        self.db.add(bookSQL)
        await self.db.commit()
    
    async def update(self, book : BookEntity) -> None:
        bookSQL = Bookmapper.to_SQL(book)
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == bookSQL.id))
        book_to_update = result.scalar_one_or_none()
        if book_to_update:
            self.db.merge(book_to_update)
            await self.db.commit()
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        book_to_delete = result.scalar_one_or_none()
        if book_to_delete:
            await self.db.delete(book_to_delete)
            await self.db.commit()
    
    async def get_by_id(self, id: int) -> Optional[BookEntity]:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        resrvation = result.scalar_one_or_none()
        return Bookmapper.to_Entity(resrvation)   
    
    async def get_all(self) -> List[BookEntity]:
        result = await self.db.execute(select(BookSQL))
        books_list = result.scalars().all()
        return list(map(Bookmapper.to_Entity,books_list))
    
    async def stock_update(self, id, new_stock) -> None:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        book = result.scalar_one_or_none()
        if book:
            bookentity = Bookmapper.to_Entity(book)
            bookentity.units += new_stock
            await self.update(bookentity)