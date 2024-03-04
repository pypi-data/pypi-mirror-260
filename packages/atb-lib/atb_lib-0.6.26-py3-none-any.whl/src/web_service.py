import asyncio
import json
import uuid
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from atb_lib.src.color_logger import ColoredLogger  # Custom logger for colored logging output


class WebService:

    def __init__(self, host: str, port: int, logger: Optional[ColoredLogger] = None):
        self._host = host
        self._port = port
        self._app = FastAPI()
        self._connections = {}
        self._subscriptions = {}
        self._logger = logger or ColoredLogger('WebService')

        origins = [f"*"]

        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self._app.websocket("/ws")
        async def _websocket_endpoint(websocket: WebSocket):
            await self._connect(websocket)
            try:
                # Keep the connection open
                while True:
                    await asyncio.sleep(10)  # Placeholder for doing something with the connection
            except WebSocketDisconnect:
                self._disconnect(websocket)

        @self._app.post("/subscribe")
        async def _subscribe(request: Request):
            data = await request.json()
            self._subscriptions[data.get("websocket_id")] = {
                "exchange_id": data.get("exchange_id"),
                "market": data.get("market"),
                "symbol": data.get("symbol"),
                "grouping_id": data.get("grouping_id")
            }
            return {"message": "Subscribed successfully"}

    async def _connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket_id = str(uuid.uuid4())  # Assigning a unique ID
        self._connections[websocket_id] = websocket
        self._logger.info(f"WebSocket connected: {websocket_id}")

        # Send the websocket_id back to the client through the WebSocket
        await websocket.send_json({"websocket_id": websocket_id})

    def _disconnect(self, websocket: WebSocket):
        #        websocket_id_for_remove = [k for k, v in self._connections.items() if v == websocket]
        #        self._subscriptions = {k:v for k, v in self._subscriptions.items() if k not in websocket_id_for_remove}
        #        self._connections = {k:v for k, v in self._connections.items() if v != websocket}
        self._logger.debug(f"WebSocket disconnected: {websocket}")

    def get_websockets_dict(self):
        websockets = {}
        for k, v in self._connections.items():
            if v not in websockets:
                websockets[v] = [k]
            else:
                websockets[v].append(k)

    async def publish_data_to_subscribed_clients(self, data):
        for websocket_id, websocket in self._connections.items():
            subscription_data = self._get_subscription_data(websocket_id, data)
            if subscription_data:
                try:
                    subscription_data_encoded = json.dumps(subscription_data)
                    await websocket.send_text(subscription_data_encoded)
                except Exception as e:
                    self._logger.debug(f"Error sending data to WebSocket: {e}")
                    self._disconnect(websocket)

    def _get_subscription_data(self, websocket_id, data):
        subscription = self._subscriptions.get(websocket_id)

        if not subscription:
            return None

        grouping_id = str(subscription['grouping_id'])

        if (
                data['exchange_id'] == subscription['exchange_id']
                and data['market'] == subscription['market']
                and data['symbol'] == subscription['symbol']
                and grouping_id in list(data['orderbooks'].keys())
        ):
            new_data = data.copy()
            new_data['orderbook'] = data['orderbooks'][grouping_id]
            del new_data['orderbooks']
            return new_data

        return None

    async def run(self):
        config = Config(self._app, host=self._host, port=self._port)
        server = Server(config)
        await server.serve()
