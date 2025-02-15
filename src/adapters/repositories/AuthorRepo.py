from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from src.domain.repositories.AuthorsABS import AuthorRepository
from src.domain.entities.Users import Author as AuthorEntity
from src.adapters.models_mappers.models import Author as AuthorSQL
from typing import Optional, List
from src.adapters.models_mappers.Authormapper import Authormapper

class SqlAlchemyAuthorRepository(AuthorRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, author: AuthorEntity) -> None:
        authorSQL = Authormapper.to_SQL(author)
        self.db.add(authorSQL)

    async def update(self, author: AuthorEntity) -> None:
        authorSQL = Authormapper.to_SQL(author)
        await self.db.merge(authorSQL)

    async def delete(self, id: int) -> None:
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == id))
        author_to_delete = result.scalar_one_or_none()
        if author_to_delete:
            await self.db.delete(author_to_delete)

    async def get_all(self) -> List[AuthorEntity]:
        result = await self.db.execute(select(AuthorSQL))
        authors_list = result.scalars().all()
        return list(map(AuthorEntity.model_validate,authors_list))

    async def get_by_id(self, id: int) -> Optional[AuthorEntity]:
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == id))
        author = result.scalar_one_or_none()
        return AuthorEntity.model_validate(author) if author else None   
        