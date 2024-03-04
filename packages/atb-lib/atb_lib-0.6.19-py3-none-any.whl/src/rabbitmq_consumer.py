from typing import Callable, Awaitable

import aio_pika

from color_logger import ColoredLogger


class RabbitMqConsumer:
    def __init__(self, rabbitmq_url: str, rabbitmq_queue_name: str,
                 callback: Callable[..., Awaitable[None]],
                 message_ttl_ms: int,
                 logger: ColoredLogger):
        """
        Initializes the RabbitMQ consumer with necessary configuration.
        """
        if not rabbitmq_url or not rabbitmq_queue_name:
            raise ValueError("RabbitMQ URL and queue name must be provided")

        self._logger = logger
        self._rabbitmq_url = rabbitmq_url
        self._queue = None
        self._queue_name = rabbitmq_queue_name
        self._callback = callback
        self._message_ttl_ms = message_ttl_ms
        self._connection = None
        self._channel = None
        self._logger.debug("RabbitMqConsumer initialized.")

    async def connect(self):
        """
        Asynchronously establishes a connection to the RabbitMQ server and sets up the queue.
        """
        try:
            self._logger.debug("Attempting to connect to RabbitMQ...")
            self._connection = await aio_pika.connect_robust(self._rabbitmq_url)
            self._logger.debug("Connection established with RabbitMQ.")

            self._channel = await self._connection.channel()
            self._logger.debug("Channel created.")

            queue_args = {'x-message-ttl': self._message_ttl_ms} if self._message_ttl_ms else {}
            self._queue = await self._channel.declare_queue(self._queue_name, arguments=queue_args)
            self._logger.debug(f"Queue '{self._queue_name}' declared successfully.")
        except Exception as e:
            self._logger.error(f"Error during RabbitMQ setup: {e}")
            raise

    async def receive_from_rabbitmq(self):
        """
        Continuously receives messages from the RabbitMQ queue.
        """
        self._logger.debug("Connected to RabbitMQ, now listening for messages.")
        self._logger.debug(f"Listening on the queue: {self._queue_name}")

        async for message in self._queue:
            try:
                await self._callback(message.body)
                await message.ack()
            except Exception as e:
                self._logger.error(f"Error processing message: {e}")
                await message.nack(requeue=True)

    async def close(self):
        """
        Closes the RabbitMQ channel and connection.
        """
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()