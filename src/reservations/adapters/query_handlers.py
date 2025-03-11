from src.reservations.domain.entities.Reservations import Reservation
from fastapi import HTTPException
from src.reservations.domain.queries import AllReservations, OneReservation
import json

class ReservationQueryHandler:

    @staticmethod
    async def get_all(query: AllReservations, repos, redis):
        cache_key = f"reservation_{query.page}_{query.per_page}"
        reservation_cached = await redis.get(cache_key)
        if reservation_cached:
            reservations_list = json.loads(reservation_cached)
        else:
            reservation_repo = repos.reservation
            reservations = await reservation_repo.get_all(query.page, query.per_page)
            reservations_list = list(Reservation.model_dump(reservation) for reservation in reservations)
            await redis.setex(cache_key,60,json.dumps(reservations_list).encode('utf-8'))
        return reservations_list
    @staticmethod
    async def get_one(query: OneReservation, repos, token, redis):
        cache_key = f"reservation_{query.reservation_id}"
        reservation_cached = await redis.get(cache_key)
        if reservation_cached:
            reservation = json.loads(reservation_cached)
        else:
            reservation_repo = repos.reservation
            reservation = await reservation_repo.get_by_id(query.reservation_id)
            await redis.setex(cache_key,60,json.dumps(Reservation.model_dump(reservation)).encode('utf-8'))
        
        if (token["role"] == "ADMIN") or (reservation.customer.user.id == int(token["user_id"])):
            return dict(reservation)
        else:
            raise HTTPException(404, detail="Not authorized")