import aio_pika

from atb_lib.src.color_logger import ColoredLogger  # Custom logger for colored logging output


class RabbitMqProducer:
    def __init__(self, rabbitmq_url: str, rabbitmq_queue_name: str,
                 message_ttl_ms: int, logger: ColoredLogger):
        if not rabbitmq_url or not rabbitmq_queue_name:
            raise ValueError("RabbitMQ URL and queue name must be provided")

        self._logger = logger
        self._rabbitmq_url = rabbitmq_url
        self._queue_name = rabbitmq_queue_name
        self._message_ttl_ms = message_ttl_ms
        self._connection = None
        self._channel = None
        self._logger.debug("RabbitMqProducer initialized.")

    async def _setup_connection(self):
        self._connection = await aio_pika.connect_robust(self._rabbitmq_url)
        self._channel = await self._connection.channel()
        queue_args = {'x-message-ttl': self._message_ttl_ms} if self._message_ttl_ms else {}
        await self._channel.declare_queue(self._queue_name, arguments=queue_args)

    async def connect(self):
        try:
            await self._setup_connection()
        except Exception as e:
            self._logger.error(f"Error during RabbitMQ setup: {e}")
            raise

    async def send_to_rabbitmq(self, message):
        if not self._channel or self._channel.is_closed:
            raise Exception("RabbitMQ channel is not open. Call connect() first.")
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=self._queue_name
        )

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()