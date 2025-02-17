from src.domain.handlers import Handlers
from src.services_layer.messagebus import RabbitMQMessageBus

class Subscribers:
    
    async def subs_usercreated(bus: RabbitMQMessageBus):
        await bus.subscribe("user.events",Handlers.usercreated_handler)
