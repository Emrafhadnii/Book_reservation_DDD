from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.repositories.ReservationABS import ReservationRepository
from src.domain.entities.Reservations import Reservation as ReservationEntity
from src.adapters.models_mappers.models import Reservation as ReservationSQL
from typing import Optional, List
from src.adapters.models_mappers.Reservationmapper import Reservationmapper
from datetime import datetime

class SqlAlchemyReservationRepository(ReservationRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, reservation: ReservationEntity) -> None:
        reservationSQL = Reservationmapper.to_SQL(reservation)
        self.db.add(reservationSQL)
    
    async def update(self, reservation : ReservationEntity) -> None:
        reservationSQL = ReservationEntity.to_SQL(reservation)
        await self.db.merge(reservationSQL)
    
    async def delete(self, id : int) -> None:
        result = await self.db.execute(select(ReservationSQL).filter(ReservationSQL.id == id))
        reservation_to_delete = result.scalar_one_or_none()
        if reservation_to_delete:
            await self.db.delete(reservation_to_delete)
    
    async def get_by_id(self, id: int) -> Optional[ReservationEntity]:
        result = await self.db.execute(select(ReservationSQL).filter(ReservationSQL.id == id))
        resrvation = result.scalar_one_or_none()
        return ReservationEntity.model_validate(resrvation)   
    
    async def get_all(self, page: int = 1, per_page: int = 5) -> List[ReservationEntity]:
        offset = (page - 1) * per_page
        result = await self.db.execute(select(ReservationSQL).limit(per_page).offset(offset))
        reservations_list = result.scalars().all()
        return list(map(ReservationEntity.model_validate, reservations_list))

    async def delete_ended_reservations(self) -> None:
        result = await self.db.execute(select(ReservationSQL.id).filter(ReservationSQL.end_time < datetime.now()))
        reservation_list = result.scalars().all()
        async for id in reservation_list:
            await self.delete(id)
