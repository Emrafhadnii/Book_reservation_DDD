from contextlib import asynccontextmanager
from typing import Type, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from logging import Logger
from setup_db.database import SessionLocal
from src.adapters.repositories.UserRepository import SqlAlchemyUserRepository
from src.adapters.repositories.BookRepo import SqlAlchemyBookRepository
from src.adapters.repositories.CustomerRepo import SqlAlchemyCustomerRepository
from src.adapters.repositories.ReservationRepo import SqlAlchemyReservationRepository
from src.adapters.repositories.AuthorRepo import SqlAlchemyAuthorRepository

class UnitOfWork:
    def __init__(self):
        self.session = SessionLocal()
        self.author = SqlAlchemyAuthorRepository(self.session)
        self.user = SqlAlchemyUserRepository(self.session)
        self.book = SqlAlchemyBookRepository(self.session)
        self.customer = SqlAlchemyCustomerRepository(self.session)
        self.reservation = SqlAlchemyReservationRepository(self.session)
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()