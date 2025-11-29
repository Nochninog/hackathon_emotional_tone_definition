import json
from typing import Any
from collections.abc import Callable

import aio_pika
from aio_pika import IncomingMessage

from ...adapters.events import IEventConsumer


class AioPikaEventConsumer(IEventConsumer):
    __amqp_url: str
    __exchange_name: str
    __prefix: str

    __connection: aio_pika.RobustConnection | None = None
    __channel: aio_pika.Channel | None = None
    __exchange: aio_pika.Exchange | None = None
    __queue: aio_pika.Queue | None = None

    __handlers: dict[str, Callable[[Any], Any]]

    def __init__(
        self,
        amqp_url: str,
        exchange_name: str = "events",
        routing_key_prefix: str = "",
        queue_name: str = "events.consumer",
    ):
        self.__amqp_url = amqp_url
        self.__exchange_name = exchange_name
        self.__prefix = routing_key_prefix
        self.__queue_name = queue_name

        self.__handlers = {}

    def register_event(
        self,
        event_name: str,
        handler: Callable[[Any], Any],
    ) -> None:
        self.__handlers[event_name] = handler

    async def connect(self) -> None:
        if self.__connection and not self.__connection.is_closed:
            return

        self.__connection = await aio_pika.connect_robust(self.__amqp_url)
        self.__channel = await self.__connection.channel()

        self.__exchange = await self.__channel.declare_exchange(
            self.__exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        self.__queue = await self.__channel.declare_queue(
            self.__queue_name,
            durable=True,
        )

        for event_name in self.__handlers.keys():
            routing_key = self.__make_routing_key(event_name)
            await self.__queue.bind(self.__exchange, routing_key)

    async def close(self) -> None:
        if self.__connection:
            await self.__connection.close()

    async def start_consuming(self) -> None:
        await self.connect()

        await self.__queue.consume(self.__on_message)

    async def __on_message(self, message: IncomingMessage) -> None:
        async with message.process():
            routing_key = message.routing_key
            event_name = self.__extract_event_name(routing_key)

            handler = self.__handlers.get(event_name)
            if not handler:
                return

            payload = self.__decode_message_payload(message.body)

            result = handler(payload)
            if hasattr(result, "__await__"):
                await result

    def __make_routing_key(self, event_name: str) -> str:
        if self.__prefix:
            return f"{self.__prefix}.{event_name}"
        return event_name

    def __extract_event_name(self, routing_key: str) -> str:
        if not self.__prefix:
            return routing_key

        prefix = f"{self.__prefix}."
        return routing_key.removeprefix(prefix)

    def __decode_message_payload(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))
