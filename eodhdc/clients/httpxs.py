# -*- coding: utf-8 -*-
from typing import Tuple
import httpx
from eodhdc import exceptions


# pylint: disable=duplicate-code
def get(url: str, params: dict, **kwargs) -> Tuple[str, bytes]:
    """Send remote request.

    :param url: request target.
    :param params: request parameters.
    :param kwargs: client arguments.
    :return: content-type and content.
    """
    try:
        response = httpx.get(url, params=params, **kwargs)
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
