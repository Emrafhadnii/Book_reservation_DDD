from src.services_layer.messagebus import RabbitMQMessageBus
from src.adapters.UOW import UnitOfWork

class BookEvents:
    async def bookisavailable_event(bus: RabbitMQMessageBus, book_id: int):
        await bus.publish(
            topic="book_isavailable",
            message={"book_id": book_id}
        )
    async def booktablechanged_event(bus: RabbitMQMessageBus, event_message: dict):
        await bus.publish(
            topic="outbox",
            message=event_message
        )