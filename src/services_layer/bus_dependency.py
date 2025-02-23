from src.services_layer.messagebus import RabbitMQMessageBus
from src.config.setting import settings

messagebus = RabbitMQMessageBus(settings.RabbitURL)

async def get_message_bus():
    return messagebus