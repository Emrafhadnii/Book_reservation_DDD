from src.services_layer.messagebus import RabbitMQMessageBus
from src.books.adapters.handlers import BookHandler
from src.users.adapters.handlers import UserHandler

class Consumers:
    async def comsuming_queues(bus: RabbitMQMessageBus):
        await bus.subscribe("user.events",UserHandler.usercreated_handler)
        await bus.subscribe("book_isavailable",BookHandler.bookisavailable_handler)
        await bus.subscribe("outbox",BookHandler.booktablechanged_event)