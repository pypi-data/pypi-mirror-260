from abc import ABC, abstractmethod
from typing import Callable, Awaitable

import websockets
import websockets.client

from color_logger import ColoredLogger


class CryptoExchangeWS(ABC):
    def __init__(self,
                 url: str,
                 callback: Callable[..., Awaitable[None]],
                 logger: ColoredLogger):

        self._ws = None
        self._url = url
        self._callback = callback
        self._logger = logger

    async def connect(self):
        self._ws = await websockets.client.connect(self._url)

    async def _receive_messages(self, message: str):
        data = self._parse_message(message)
        await self._callback(data)

    @abstractmethod
    def _parse_message(self, message):
        pass

    async def run_forever(self):
        await self.connect()
        while True:
            message = await self._ws.recv()
            await self._receive_messages(message)

    async def close(self):
        if self._ws and not self._ws.closed:
            await self._ws.close()
