from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.Users import Customer
from src.domain.enums import SubscriptionModel
from datetime import datetime
from src.domain.repositories.first_layer_ABS import FirstAbstractionLayer

class CustomerRepository(FirstAbstractionLayer[Customer]):

    @abstractmethod
    def change_subscription(self,user_id: int,new_model: SubscriptionModel,end_date: datetime) -> Customer:
        pass

    @abstractmethod
    def add_to_wallet(self, user_id: int, amount: float) -> Customer:
        pass