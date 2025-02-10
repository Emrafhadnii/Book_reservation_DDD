from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.Users import User
from first_layer_ABS import FirstAbstractionLayer

class UserRepository(ABC,FirstAbstractionLayer[User]):

    @abstractmethod
    def get_role(self, id:int) -> User:
        pass

   