from __future__ import annotations

import json
from typing import Any

import aio_pika
from aio_pika import DeliveryMode, Message

from ...adapters.events import IEventPublisher


class AioPikaEventPublisher(IEventPublisher):
    __amqp_url: str
    __exchange_name: str
    __prefix: str

    __connection: aio_pika.abc.AbstractRobustConnection | None = None
    __channel: aio_pika.abc.AbstractChannel | None = None
    __exchange: aio_pika.abc.AbstractExchange | None = None

    def __init__(
        self,
        amqp_url: str,
        exchange_name: str = "events",
        routing_key_prefix: str = "",
    ) -> None:
        self.__amqp_url = amqp_url
        self.__exchange_name = exchange_name
        self.__prefix = routing_key_prefix

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

    async def close(self) -> None:
        if self.__connection:
            await self.__connection.close()

    @property
    def _exchange(self) -> aio_pika.abc.AbstractExchange:
        if self.__exchange is None:
            raise Exception("Does not have exchange")
        return self.__exchange

    async def publish_event(
        self,
        event_name: str,
        data: Any,
    ) -> None:
        await self.connect()

        routing_key = self.__make_routing_key(event_name)
        payload = self.__encode_message_payload(data)

        message = Message(
            body=payload,
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
        )

        await self._exchange.publish(
            message=message,
            routing_key=routing_key,
        )

    def __make_routing_key(self, event_name: str) -> str:
        if self.__prefix:
            return f"{self.__prefix}.{event_name}"
        return event_name

    def __encode_message_payload(self, payload: Any) -> bytes:
        return json.dumps(
            payload,
            default=str,
        ).encode("utf-8")
