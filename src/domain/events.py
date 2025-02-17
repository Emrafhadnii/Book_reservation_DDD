from src.domain.entities.Users import User
from src.services_layer.messagebus import RabbitMQMessageBus



class Events:
    
    async def usercreated_event(bus: RabbitMQMessageBus, user: User):
        message = {
            "user": user,
            "event": "user.created"
        }
        await bus.publish(topic="user.events",message=message)
        