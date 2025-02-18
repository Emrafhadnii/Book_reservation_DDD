import json
from aio_pika import connect, Message, ExchangeType
from typing import Callable, Dict, Any




class RabbitMQMessageBus():
    def __init__(self, connection_str: str):
        self.connection_str = connection_str
        self.connection = None
        self.channel = None
        self.exchanges = {}
        self.queues = {}

    async def connect(self):
        self.connection = await connect(self.connection_str)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        return self

    async def publish(self, topic: str, message: Dict[str, Any], priority: int = 0):
        exchange = await self._get_exchange(topic)
        await exchange.publish(
            Message(
                body=json.dumps(message).encode(),
                priority=priority,
                delivery_mode=1
            ),
            routing_key=topic
        )

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Any]):
        exchange = await self._get_exchange(topic)
        queue = await self._get_queues(topic)
        await queue.bind(exchange, routing_key=topic)
        self.queues[topic]['callback'] = callback

    async def consume_queue(self, topic: str):
        if topic not in self.queues:
            raise ValueError(f"No queue found for topic: {topic}")
        queue = self.queues[topic]['queue']
        callback = self.queues[topic]['callback']
        if topic == "reservation_queue":
            message = await queue.get()
            if message:
                try:
                    async with message.process():
                        data = json.loads(message.body.decode())
                        await callback(data)
                        await message.ack()
                except Exception as e:
                    await message.nack(requeue=False)
        else:
            await queue.consume(lambda msg: self._handle_message(msg, callback))
        


    async def _get_queues(self, topic: str):
        if topic not in self.queues:
            self.queues[topic] = {}
            self.queues[topic]['queue'] = await self.channel.declare_queue(
            name=topic,
            exclusive=True,
            arguments={'x-max-priority': 3}
            )
        return self.queues[topic]['queue']

    async def _get_exchange(self, topic: str):
        if topic not in self.exchanges:
            self.exchanges[topic] = await self.channel.declare_exchange(
                topic, ExchangeType.TOPIC, durable=True
            )
        return self.exchanges[topic]

    async def _handle_message(self, message, callback):
        try:
            async with message.process():
                data = json.loads(message.body.decode())
                await callback(data)
        except Exception as e:
            pass