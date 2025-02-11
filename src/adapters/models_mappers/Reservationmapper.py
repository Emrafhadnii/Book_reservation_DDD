from models import Reservation
from src.domain.entities.Reservation import Reservation as ReservationEntity

class Reservationmapper:
    def to_Entity(dbmodel:Reservation) -> ReservationEntity:
        return ReservationEntity(id=dbmodel.id,book=dbmodel.book,customer=dbmodel.customer,price=dbmodel.price,
                                 start_time=dbmodel.start_time,end_time=dbmodel.end_time
                                 )
    def to_SQL(dbmodel: ReservationEntity) -> Reservation:
        return Reservation(id=dbmodel.id, book=dbmodel.book, customer=dbmodel.customer, price=dbmodel.price,
                        start_time=dbmodel.start_time, end_time=dbmodel.end_time)
