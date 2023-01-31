# -*- coding: utf-8 -*-
from typing import Tuple
import httpx
from eodhdc import exceptions


# pylint: disable=duplicate-code
async def get(session: httpx.AsyncClient, url: str, params: dict, **kwargs) -> Tuple[str, bytes]:
    """Send remote request.

    :param session: session object.
    :param url: request target.
    :param params: request parameters.
    :param kwargs: client arguments.
    :return: content-type and content.
    """
    try:
        response = await session.get(url, params=params, **kwargs)
        response.raise_for_status()
        return response.headers["content-type"].split(";")[0], response.content
    except httpx.HTTPStatusError as ex:
        raise exceptions.ClientHTTPError(ex.response.status_code, ex) from None
    except httpx.TimeoutException as ex:
        raise exceptions.ClientConnectionTimeout(ex) from None
    except (httpx.NetworkError, httpx.ProtocolError) as ex:
        raise exceptions.ClientConnectionError(ex) from None
    except httpx.HTTPError as ex:
        raise exceptions.ClientException(ex) from None


def create() -> httpx.AsyncClient:
    """Create async session to make it reusable for optimal performance.

    :return: session object.
    """
    return httpx.AsyncClient()


async def destroy(session: httpx.AsyncClient):
    """Destroy previously created async session.

    :param session: session object.
    """
    await session.aclose()
