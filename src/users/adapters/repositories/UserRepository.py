from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.users.domain.repositories.UserABS import UserRepository
from src.users.domain.entities.Users import User as UserEntity
from src.users.adapters.models.Usermodel import User
from typing import Optional, List
from src.users.adapters.mappers.Usermapper import Usermapper
from src.auth.domain.entities.auth import emailResponsemodel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db 

    async def get_by_id(self, id: int) -> Optional[UserEntity]:
        result = await self.db.execute(select(User).filter(User.id == id))
        user = result.scalar_one_or_none()
        return UserEntity.model_validate(user)
    
    async def get_all(self, page: int = 1, per_page: int = 5) -> List[UserEntity]:
        offset = (page - 1) * per_page
        result = await self.db.execute(select(User).limit(per_page).offset(offset))
        users_list = result.scalars().all()
        return list(map(UserEntity.model_validate, users_list))


    async def delete(self, id: int) -> None:
        result = await self.db.execute(select(User).filter(User.id == id))
        user_to_delete = result.scalar_one_or_none()
        if user_to_delete:
            await self.db.delete(user_to_delete)

    async def update(self, user: UserEntity) -> None:
        reservationSQL = UserEntity.to_SQL(user)
        await self.db.merge(reservationSQL)

    async def add(self, t: UserEntity) -> None:
        userSQL = Usermapper.to_SQL(t)
        self.db.add(userSQL)

    async def get_role(self, id: int) -> str:
        result = await self.db.execute(select(User).filter(User.id == id))
        role = result.scalar_one_or_none()
        if not role:
            raise ValueError(f"User with id {id} not found")
        return role.user_role
    
    async def get_by_phone(self, phone) -> emailResponsemodel:
        result = await self.db.execute(select(User).filter(User.phone == phone))
        user = result.scalar_one_or_none()
        if user:
            return emailResponsemodel(phone=user.phone, id=user.id, user_role=user.user_role,password=user.user_password)
        else:
            raise ValueError(f"User with phone {phone} not found")
    
    async def get_by_phone_all(self, phone) -> UserEntity:
        result = await self.db.execute(select(User).filter(User.phone == phone))
        user = result.scalar_one_or_none()
        return UserEntity.model_validate(user) if user else None