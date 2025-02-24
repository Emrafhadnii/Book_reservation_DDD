from src.reservations.adapters.models.mongo_models.Mongo_Reservationmodel import Reservation as mongoReservation
from src.reservations.domain.entities.Reservations import Reservation

class MongoReservationMapper:
    
    @staticmethod
    def to_Mongo(reservation: Reservation) -> mongoReservation:
        return mongoReservation(
            id=reservation.id,
            customer_id=reservation.customer.user.id,
            book_id=reservation.book.id,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            price=reservation.price
        )
    @staticmethod
    def to_Entity(reservation:mongoReservation) -> Reservation:
        return Reservation(
            """
            idk how to deploy this
            """
        )