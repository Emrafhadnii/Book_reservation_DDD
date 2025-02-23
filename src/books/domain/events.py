from src.services_layer.messagebus import RabbitMQMessageBus

class BookEvents:
    async def bookisavailable_event(bus: RabbitMQMessageBus, book_id: int):
        await bus.publish(
            topic="book_isavailable",
            message={"book_id": book_id}
        )