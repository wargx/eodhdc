# -*- coding: utf-8 -*-
import asyncio
from eodhdc import EODHDClient
from eodhdc import EODHDWebSockets


async def coro():
    """ asynchronous """
    print("--------------- coro playground ---------------")
    eodhdc = EODHDClient("httpxa")
    async with eodhdc.session:
        results = await asyncio.gather(
            eodhdc.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10", fmt="csv"),
            eodhdc.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10", fmt="json")
        )
    for result in results:
        print(result)
    print("--------------- --------------- ---------------")


def sync():
    """ synchronous """
    print("--------------- sync playground ---------------")
    eodhdc = EODHDClient("requests")
    result = eodhdc.market.historical(
        "AAPL.US", start="2023-01-01", finish="2023-01-10",
        fmt="json", output="pandas:./response.tex", writer={"header": False}
    )
    print(result, "\n")

    result = eodhdc.market.historical(
        "MCD.US", start="2022-01-01", finish="2022-01-10",
        fmt="csv", output="pandas:./response.csv", writer={
            "change:columns": {
                "Date": "date", "Open": "open", "High": "high", "Low": "low",
                "Close": "close", "Volume": "volume", "Adjusted_close": "adjcp"
            }, "change:reorder": True, "change:reindex": "date"
        }
    )
    print(result)
    print("--------------- --------------- ---------------")


async def wssc():
    """ websockets """
    print("--------------- wssc playground ---------------")
    eodhdws = EODHDWebSockets(buffer=100)
    async with eodhdws.connect("us") as websocket:
        await eodhdws.subscribe(websocket, ["TSLA", "EURUSD"])
        async for message in eodhdws.receive(websocket):
            print(message)
            if len(eodhdws.buffer) > 5:
                await eodhdws.unsubscribe(websocket, ["EURUSD"])
            if len(eodhdws.buffer) > 10:
                eodhdws.deactivate()

    print(eodhdws.buffer)
    print("--------------- --------------- ---------------")


asyncio.run(coro())
sync()
asyncio.run(wssc())
