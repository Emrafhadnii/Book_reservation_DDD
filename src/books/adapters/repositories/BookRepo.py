from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.books.domain.repositories.BookABS import BookRepository
from src.books.domain.entities.Books import Book as BookEntity
from src.books.adapters.models.Bookmodel import Book as BookSQL
from typing import Optional, List
from src.books.adapters.mappers.Bookmapper import Bookmapper


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
    
    async def get_all(self, page: int = 1, per_page: int = 5) -> List[BookEntity]:
        offset = (page-1)*per_page
        result = await self.db.execute(select(BookSQL).limit(per_page).offset(offset))
        books_list = result.scalars().all()
        return list(map(BookEntity.model_validate,books_list))

    async def stock_update(self, id: int, new_stock: int) -> None:
        result = await self.db.execute(select(BookSQL).filter(BookSQL.id == id))
        book = result.scalar_one_or_none()
        if book:
            bookentity = BookEntity.model_validate(book)
            bookentity.units += new_stock
            await self.update(bookentity)