from abc import abstractmethod
from src.users.domain.entities.Users import User
from src.adapters.repositories.first_layer_ABS import FirstAbstractionLayer
from src.auth.domain.entities.auth import emailResponsemodel


class UserRepository(FirstAbstractionLayer[User]):

    @abstractmethod
    def get_role(self, id:int) -> str:
        pass

    @abstractmethod
    def get_by_phone(self, phone:str) -> emailResponsemodel:
        pass

   