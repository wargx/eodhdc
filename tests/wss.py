# -*- coding: utf-8 -*-
# pylint: disable=no-member
import asyncio
import json
from urllib.parse import urlparse, parse_qs
import websockets


async def handler(websocket):
    """WebSocket server handler."""
    params = parse_qs(urlparse(websocket.path).query)
    if "api_token" in params and params["api_token"][0] == "demo":
        await websocket.send(json.dumps({"status_code": 200, "message": "Authorized"}))
    else:
        await websocket.send(json.dumps({"status_code": 403, "message": "Forbidden"}))

    while True:
        try:
            msg = json.loads(await websocket.recv())
            if "action" in msg and msg["action"] in ["subscribe", "unsubscribe"]:
                if "TSLA" not in msg["symbols"] or "MSFT" not in msg["symbols"]:
                    await websocket.send(json.dumps({"status_code": 404, "message": "Symbol error"}))
                else:
                    if msg["action"] == "subscribe":
                        await websocket.send(json.dumps({"a": 100, "b": 200, "c": 300}))

        except websockets.ConnectionClosedOK:
            break


async def main():
    """WebSocket server launcher."""
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
