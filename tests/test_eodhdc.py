# -*- coding: utf-8 -*-
import os
import asyncio
import pytest
from eodhdc.clients import aiohttp, httpxa
from eodhdc.clients import httpxs, requests
from eodhdc import EODHDClient, exceptions


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """Set cassettes path."""
    return os.path.join("tests", "cassettes", request.module.__name__.split(".")[-1])


@pytest.mark.eodhdc
@pytest.mark.parametrize("client, exception", [
    ["unknown", exceptions.UnknownClient],
    [exceptions, exceptions.ImproperClient]
])
def test_eodhdc_exceptions(client, exception):
    """Module exceptions tests."""
    with pytest.raises(exception):
        _ = EODHDClient(client)


@pytest.mark.eodhdc
@pytest.mark.parametrize("client, mode, module", [
    ["httpxs", "sync", httpxs],
    ["requests", "sync", requests]
])
def test_eodhdc_init_sync(client, mode, module):
    """Client sync mode initialization tests."""
    eodhd = EODHDClient(client)
    assert eodhd.mode == mode
    assert eodhd.client == module


@pytest.mark.asyncio
@pytest.mark.eodhdc
@pytest.mark.parametrize("client, mode, module, session", [
    ["httpxa", "coro", httpxa, httpxa.httpx.AsyncClient],
    ["aiohttp", "coro", aiohttp, aiohttp.aiohttp.ClientSession],
    [aiohttp, "coro", aiohttp, aiohttp.aiohttp.ClientSession]
])
async def test_eodhdc_init_async(client, mode, module, session):
    """Client async mode initialization tests."""
    eodhd = EODHDClient(client)
    assert eodhd.mode == mode
    assert eodhd.client == module
    assert isinstance(eodhd.session, session)


@pytest.mark.eodhdc
@pytest.mark.vcr()
def test_eodhdc_flow_sync():
    """Client sync flow test."""
    eodhd = EODHDClient("httpxs")
    _ = eodhd.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10")


@pytest.mark.asyncio
@pytest.mark.eodhdc
@pytest.mark.vcr()
async def test_eodhdc_flow_async():
    """Client async flow test."""
    eodhd = EODHDClient("aiohttp")
    async with eodhd.session:
        _ = await asyncio.gather(
            eodhd.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10", fmt="csv")
        )
    await eodhd.destroy()
