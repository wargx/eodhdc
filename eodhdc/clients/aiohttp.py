# -*- coding: utf-8 -*-
from typing import Tuple
import asyncio
import aiohttp
from eodhdc import exceptions


async def get(session: aiohttp.ClientSession, url: str, params: dict, **kwargs) -> Tuple[str, bytes]:
    """Send remote request.

    :param session: session object.
    :param url: request target.
    :param params: request parameters.
    :param kwargs: client arguments.
    :return: content-type and content.
    """
    try:
        async with session.get(url, params=params, **kwargs) as response:
            response.raise_for_status()
            return response.content_type, await response.content.read()
    except aiohttp.ClientResponseError as ex:
        raise exceptions.ClientHTTPError(ex.status, ex.message) from None
    except asyncio.TimeoutError as ex:
        raise exceptions.ClientConnectionTimeout(ex) from None
    except aiohttp.ClientConnectionError as ex:
        raise exceptions.ClientConnectionError(ex) from None
    except Exception as ex:
        raise exceptions.ClientException(ex) from None


def create() -> aiohttp.ClientSession:
    """Create async session to make it reusable for optimal performance.

    :return: session object.
    """
    return aiohttp.ClientSession()


async def destroy(session: aiohttp.ClientSession):
    """Destroy previously created async session.

    :param session: session object.
    """
    await session.close()
