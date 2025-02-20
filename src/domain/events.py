from src.domain.entities.Users import User
from src.services_layer.messagebus import RabbitMQMessageBus
from src.domain.handlers import Handlers
from redis import Redis


class Events:
    
    async def usercreated_event(bus: RabbitMQMessageBus, user: User):
        message = {
            "user": user,
            "event": "user.created"
        }
        await bus.publish(topic="user.events",message=message)
        
    async def bookisavailable_event(bus: RabbitMQMessageBus, book_id: int):
        await bus.publish(
            topic="book_isavailable",
            message={"book_id": book_id}
        )
        