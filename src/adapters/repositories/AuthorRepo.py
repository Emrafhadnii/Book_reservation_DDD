from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.AuthorsABS import AuthorRepository
from src.domain.entities.Users import Author as AuthorEntity
from src.adapters.models_mappers.models import Author as AuthorSQL
from typing import Optional, List
from src.adapters.models_mappers.Authormapper import Authormapper
from setup_db.database import asyncsession

class SqlAlchemyAuthorRepository(AuthorRepository):
    def __init__(self, db: AsyncSession = asyncsession):
        self.db = db

    async def add(self, author: AuthorEntity) -> None:
        authorSQL = Authormapper.to_SQL(author)
        self.db.add(authorSQL)
        await self.db.commit()
    
    async def update(self, author : AuthorEntity) -> None:
        authorSQL = Authormapper.to_SQL(author)
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == authorSQL.id))
        author_to_update = result.scalar_one_or_none()
        if author_to_update:
            self.db.merge(author_to_update)
            await self.db.commit()
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == id))
        author_to_delete = result.scalar_one_or_none()
        if author_to_delete:
            await self.db.delete(author_to_delete)
            await self.db.commit()
    
    async def get_by_id(self, id: int) -> Optional[AuthorEntity]:
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == id))
        resrvation = result.scalar_one_or_none()
        return Authormapper.to_Entity(resrvation)   
    
    async def get_all(self) -> List[AuthorEntity]:
        result = await self.db.execute(select(AuthorSQL))
        authors_list = result.scalars().all()
        return list(map(Authormapper.to_Entity,authors_list))