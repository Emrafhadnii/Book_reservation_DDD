from abc import ABC, abstractmethod
from typing import Optional, TypeVar, List, Generic, Type

T = TypeVar('T')

class FirstAbstractionLayer(ABC, Generic[T]):
  
    @abstractmethod
    def get_by_id(self, id : int) -> Optional[T] :
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def delete(self, id : int) -> None:
        pass

    @abstractmethod
    def update(self, t : T) -> None:
        pass

    @abstractmethod
    def add(self, t : T) -> None:
        pass

