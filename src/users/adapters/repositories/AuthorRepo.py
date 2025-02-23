from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.users.domain.repositories.AuthorsABS import AuthorRepository
from src.users.domain.entities.Users import Author as AuthorEntity
from src.users.adapters.models.Authormodel import Author as AuthorSQL
from typing import Optional, List
from src.users.adapters.mappers.Authormapper import Authormapper

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

    async def get_all(self, page: int = 1, per_page: int = 5) -> List[AuthorEntity]:
        offset = (page-1)*per_page
        result = await self.db.execute(select(AuthorSQL).limit(per_page).offset(offset))
        authors_list = result.scalars().all()
        return list(map(AuthorEntity.model_validate, authors_list))

    async def get_by_id(self, id: int) -> Optional[AuthorEntity]:
        result = await self.db.execute(select(AuthorSQL).filter(AuthorSQL.id == id))
        author = result.scalar_one_or_none()
        return AuthorEntity.model_validate(author) if author else None   
        