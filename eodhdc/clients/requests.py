# -*- coding: utf-8 -*-
from typing import Tuple
import requests
from eodhdc import exceptions


def get(url: str, params: dict, **kwargs) -> Tuple[str, bytes]:
    """Send remote request.

    :param url: request target.
    :param params: request parameters.
    :param kwargs: client arguments.
    :return: content-type and content.
    """
    try:
        response = requests.get(url, params, **kwargs)
        response.raise_for_status()
        return response.headers["content-type"].split(";")[0], response.content
    except requests.exceptions.HTTPError as ex:
        raise exceptions.ClientHTTPError(ex.response.status_code, ex) from None
    except requests.exceptions.Timeout as ex:
        raise exceptions.ClientConnectionTimeout(ex) from None
    except requests.exceptions.ConnectionError as ex:
        raise exceptions.ClientConnectionError(ex) from None
    except requests.exceptions.RequestException as ex:
        raise exceptions.ClientException(ex) from None
