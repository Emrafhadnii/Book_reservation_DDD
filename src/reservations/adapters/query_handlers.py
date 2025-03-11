from src.reservations.domain.entities.Reservations import Reservation
from fastapi import HTTPException
from src.reservations.domain.queries import AllReservations

class ReservationQueryHandler:

    @staticmethod
    async def get_all(query: AllReservations, repos):
        reservation_repo = repos.reservation
        reservations = await reservation_repo.get_all(query.page, query.per_page)
        return list(Reservation.model_validate(reservation) for reservation in reservations)
    
    @staticmethod
    async def get_one(query, repos, token):
        reservation_repo = repos.reservation
        reservation = await reservation_repo.get_by_id(query.reservation_id)
        if (token["role"] == "ADMIN") or (reservation.customer.user.id == int(token["user_id"])):
            return dict(reservation)
        else:
            raise HTTPException(404, detail="Not authorized")