from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.ReservationABS import ReservationRepository
from src.domain.entities.Reservation import Reservation as ReservationEntity
from src.adapters.models_mappers.models import Reservation as ReservationSQL
from typing import Optional, List
from src.adapters.models_mappers.Reservationmapper import Reservationmapper
from setup_db.database import asyncsession
from datetime import datetime

class SqlAlchemyBookRepository(ReservationRepository):
    def __init__(self, db: AsyncSession = asyncsession):
        self.db = db

    async def add(self, reservation: ReservationEntity) -> None:
        reservationSQL = Reservationmapper.to_SQL(reservation)
        self.db.add(reservationSQL)
        await self.db.commit()
    
    async def update(self, reservation : ReservationEntity) -> None:
        reservationSQL = Reservationmapper.to_SQL(reservation)
        result = await self.db.execute(select(ReservationSQL).filter(ReservationSQL.id == reservationSQL.id))
        reservation_to_update = result.scalar_one_or_none()
        if reservation_to_update:
            self.db.merge(reservation_to_update)
            await self.db.commit()
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(ReservationSQL).filter(ReservationSQL.id == id))
        reservation_to_delete = result.scalar_one_or_none()
        if reservation_to_delete:
            await self.db.delete(reservation_to_delete)
            await self.db.commit()
    
    async def get_by_id(self, id: int) -> Optional[ReservationEntity]:
        result = await self.db.execute(select(ReservationSQL).filter(ReservationSQL.id == id))
        resrvation = result.scalar_one_or_none()
        return Reservationmapper.to_Entity(resrvation)   
    
    async def get_all(self) -> List[ReservationEntity]:
        result = await self.db.execute(select(ReservationSQL))
        reservations_list = result.scalars().all()
        return list(map(Reservationmapper.to_Entity,reservations_list))

    async def delete_ended_reservations(self) -> None:
        result = await self.db.execute(select(ReservationSQL.id).filter(ReservationSQL.end_time < datetime.now()))
        reservation_list = result.scalars().all()
        async for id in reservation_list:
            await self.delete(id)
