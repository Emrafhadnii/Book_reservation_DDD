from src.adapters.models_mappers.models import Reservation
from src.domain.entities.Reservations import Reservation as ReservationEntity

class Reservationmapper:
    def to_SQL(dbmodel: ReservationEntity) -> Reservation:
        return Reservation(book_id=dbmodel.book.id, customer_id=dbmodel.customer.user.id, price=dbmodel.price,
                        start_time=dbmodel.start_time, end_time=dbmodel.end_time)
