from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from src.domain.entities.Reservation import Reservation
from first_layer_ABS import FirstAbstractionLayer

class ReservationRepository(ABC,FirstAbstractionLayer[Reservation]):

    @abstractmethod
    def delete_ended_reservations(self, reservation_id: int,start_date: datetime,end_date: datetime) -> List[Reservation]:
        pass