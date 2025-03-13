from src.services_layer.messagebus import RabbitMQMessageBus
from src.users.domain.enums import SubscriptionModel

class ReservationEvents:
    
    async def queue_event(bus: RabbitMQMessageBus, message: dict):
        await bus.publish("reservation.queue",
                          message=message
                          )