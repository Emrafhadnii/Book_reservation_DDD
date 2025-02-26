from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from src.reservations.domain.entities.Reservations import Reservation
from src.adapters.repositories.first_layer_ABS import FirstAbstractionLayer

class ReservationRepository(FirstAbstractionLayer[Reservation]):

    @abstractmethod
    def delete_ended_reservations(self, reservation_id: int,start_date: datetime,end_date: datetime) -> List[Reservation]:
        pass