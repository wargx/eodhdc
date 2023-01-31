# -*- coding: utf-8 -*-
from typing import List
import json
from collections import deque
import websockets
from eodhdc import exceptions


class EODHDWebSockets:
    """EODHD WebSockets client class"""

    def __init__(self, key: str = "demo", buffer: [int, bool] = False, args: dict = None):
        """
        :param key: api token.
        :param buffer: enable and set buffer size.
        :param args: websocket connection arguments.
        """
        self.key = key
        self.args = args or {}
        self.base = "wss://ws.eodhistoricaldata.com/ws"
        self.authorized = False
        self.active = False
        self.subscriptions = set()
        self.buffer = deque(maxlen=buffer)

    def connect(self, endpoint):
        """Connect to web-socket endpoint.

        :param endpoint: endpoint name:
            "us", "us-quote", "forex", "crypto", "index"
        :return: websocket connection.
        """
        if endpoint not in ["us", "us-quote", "forex", "crypto", "index"]:
            raise exceptions.WebsocketUnknownEndpoint(f"Unknown endpoint '{endpoint}'")
        # pylint: disable=no-member
        return websockets.connect(f"{self.base}/{endpoint}?api_token={self.key}", **self.args)

    async def authorize(self, websocket):
        """Check authorization status.

        :param websocket: websocket connection.
        """
        if not self.authorized:
            msg = json.loads(await websocket.recv())
            if not msg.get("status_code", None) == 200 and not msg["message"] == "Authorized":
                raise exceptions.WebsocketAuthError(msg["message"])
            self.authorized = True

    async def subscribe(self, websocket, symbols: List[str], auto: bool = True):
        """Subscribe to the tickers, API will ignore unknown.

        :param websocket: websocket connection.
        :param symbols: tickers list.
        :param auto: automatically activate message loop.
        """
        await self.authorize(websocket)
        await websocket.send(json.dumps({"action": "subscribe", "symbols": ", ".join(symbols)}))
        self.subscriptions.update(symbols)
        if auto:
            self.active = bool(self.subscriptions)

    async def unsubscribe(self, websocket, symbols: List[str], auto: bool = True):
        """Unsubscribe from the tickers.

        :param websocket: websocket connection.
        :param symbols: tickers list.
        :param auto: automatically activate message loop.
        """
        await self.authorize(websocket)
        await websocket.send(json.dumps({"action": "unsubscribe", "symbols": ", ".join(symbols)}))
        self.subscriptions.difference_update(symbols)
        if auto:
            self.active = bool(self.subscriptions)

    async def receive(self, websocket):
        """Receive messages.

        :param websocket: websocket connection.
        :return: async generator.
        """
        await self.authorize(websocket)
        while self.active:
            msg = json.loads(await websocket.recv())
            if "status" in msg or "status_code" in msg:
                code = msg.get("status_code", msg.get("status", None))
                raise exceptions.WebsocketResponseError(code, msg["message"])
            if self.buffer.maxlen != 0:
                self.buffer.append(msg)
            yield msg

    def activate(self):
        """Activate message loop."""
        self.active = True

    def deactivate(self):
        """Deactivate message loop."""
        self.active = False
