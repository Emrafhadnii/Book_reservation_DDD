from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.Users import User
from src.domain.repositories.first_layer_ABS import FirstAbstractionLayer
from src.domain.entities.auth import emailResponsemodel


class UserRepository(FirstAbstractionLayer[User]):

    @abstractmethod
    def get_role(self, id:int) -> str:
        pass

    @abstractmethod
    def get_by_phone(self, phone:str) -> emailResponsemodel:
        pass

   