import json
from aio_pika import connect, Message, ExchangeType
from typing import Callable, Dict, Any

class RabbitMQMessageBus():
    def __init__(self, connection_str: str):
        self.connection_str = connection_str
        self.connection = None
        self.channel = None
        self.exchanges = {}

    async def connect(self):
        self.connection = await connect(self.connection_str)
        self.channel = await self.connection.channel()
        return self

    async def publish(self, topic: str, message: Dict[str, Any], priority: int = 0):
        exchange = await self._get_exchange(topic)
        await exchange.publish(
            Message(
                body=json.dumps(message).encode(),
                priority=priority
            ),
            routing_key=topic
        )

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Any]):
        exchange = await self._get_exchange(topic)
        queue = await self.channel.declare_queue(exclusive=True)
        await queue.bind(exchange, routing_key=topic)
        await queue.consume(lambda msg: self._handle_message(msg, callback))

    async def _get_exchange(self, topic: str):
        if topic not in self.exchanges:
            self.exchanges[topic] = await self.channel.declare_exchange(
                topic, ExchangeType.TOPIC, durable=True
            )
        return self.exchanges[topic]

    async def _handle_message(self, message, callback):
        async with message.process():
            data = json.loads(message.body.decode())
            await callback(data)
