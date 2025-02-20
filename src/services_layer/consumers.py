from src.services_layer.messagebus import RabbitMQMessageBus
from src.domain.handlers import Handlers

class Consumers:
    async def comsuming_queues(bus: RabbitMQMessageBus):
        await bus.subscribe("user.events",Handlers.usercreated_handler)
        await bus.subscribe("book_isavailable",Handlers.bookisavailable_handler)