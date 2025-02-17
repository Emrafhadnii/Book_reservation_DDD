from src.services_layer.messagebus import RabbitMQMessageBus

messagebus = RabbitMQMessageBus("amqp://guest:guest@localhost")

async def get_message_bus():
    return messagebus