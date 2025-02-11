from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.UserABS import UserRepository
from src.domain.entities.Users import User as UserEntity
from src.adapters.models_mappers.models import User
from typing import Optional, List
from src.adapters.models_mappers.Usermapper import Usermapper
from setup_db.database import asyncsession


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession = asyncsession):
        self.db = db 

    async def get_by_id(self, id: int) -> Optional[UserEntity]:
        result = await self.db.execute(select(User).filter(User.id == id))
        user = result.scalar_one_or_none()
        return Usermapper.to_Entity(user)
    
    async def get_all(self) -> List[UserEntity]:
        result = await self.db.execute(select(User))
        users_list = result.scalars().all()
        return list(map(Usermapper.to_Entity,users_list))

    async def delete(self, id: int) -> None:
        result = await self.db.execute(select(User).filter(User.id == id))
        user_to_delete = result.scalar_one_or_none()
        if user_to_delete:
            await self.db.delete(user_to_delete)
            await self.db.commit()

    async def update(self, t: UserEntity) -> None:
        userSQL = Usermapper.to_SQL(t)
        result = await self.db.execute(select(User).filter(User.id == userSQL.id))
        user_to_update = result.scalar_one_or_none()
        if user_to_update:
            self.db.merge(user_to_update)
            await self.db.commit()

    async def add(self, t: UserEntity) -> None:
        userSQL = Usermapper.to_SQL(t)
        self.db.add(userSQL)
        await self.db.commit()

    async def get_role(self, id: int) -> str:
        result = await self.db.execute(select(User).filter(User.id == id))
        role = result.scalar_one_or_none()
        if not role:
            raise ValueError(f"User with id {id} not found")
        return role.user_role