# -*- coding: utf-8 -*-
# pylint: disable=consider-using-with
import subprocess
import time
import pytest
from eodhdc import EODHDWebSockets, exceptions


@pytest.mark.asyncio
@pytest.mark.eodhdws
@pytest.mark.parametrize("case", [
    [dict(key="demo"), "uk", ["TSLA"], exceptions.WebsocketUnknownEndpoint],
    [dict(key="demo1"), "us", ["TSLA"], exceptions.WebsocketAuthError],
    [dict(key="demo"), "us", ["TSLA1"], exceptions.WebsocketResponseError]
])
async def test_eodhdws_exceptions(case):
    """Module exceptions tests."""
    wss = subprocess.Popen(["python", "tests/wss.py"])
    time.sleep(0.3)
    with pytest.raises(case[3]):
        eodhdws = EODHDWebSockets(**case[0])
        eodhdws.base = "ws://127.0.0.1:8001/ws"
        async with eodhdws.connect(case[1]) as websocket:
            await eodhdws.subscribe(websocket, case[2])
            await eodhdws.receive(websocket).__anext__()
    wss.terminate()


@pytest.mark.asyncio
@pytest.mark.eodhdws
async def test_eodhdws_flow():
    """Client flow test."""
    wss = subprocess.Popen(["python", "tests/wss.py"])
    time.sleep(0.3)
    eodhdws = EODHDWebSockets(buffer=10)
    eodhdws.base = "ws://127.0.0.1:8001/ws"
    async with eodhdws.connect("us") as websocket:
        eodhdws.activate()
        await eodhdws.subscribe(websocket, ["TSLA", "MSFT"])
        await eodhdws.unsubscribe(websocket, ["MSFT"])
        async for msg in eodhdws.receive(websocket):
            assert len(msg)
            eodhdws.deactivate()
        assert len(eodhdws.buffer)
    wss.terminate()
