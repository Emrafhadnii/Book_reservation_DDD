from abc import ABC, abstractmethod
from typing import Any, Dict, Callable

class MessageBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any], priority: int = 0):
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Any]):
        pass

    @abstractmethod
    async def enqueue(self, queue: str, message: Dict[str, Any], priority: int = 0):
        pass

    @abstractmethod
    async def process_queue(self, queue: str, callback: Callable[[Dict[str, Any]], Any]):
        pass