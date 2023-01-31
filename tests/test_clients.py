# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
import os
import pytest
from eodhdc import clients, exceptions

modules = ["requests", "httpxs"]
timeouts = {"requests": (5, 5), "httpxs": (5, 5)}

cases = []
for module in modules:
    cases.extend(
        [
            (module, "-", exceptions.ClientException, None),
            [module, "https://no.domain", exceptions.ClientConnectionError, None],
            [module, "https://httpstat.us/504?sleep=60000", exceptions.ClientConnectionTimeout, None],
            [module, "https://httpbin.org/status/403", exceptions.ClientHTTPError, 403],
            [module, "https://httpbin.org/status/404", exceptions.ClientHTTPError, 404],
            [module, "https://httpbin.org/status/500", exceptions.ClientHTTPError, 500]
        ]
    )


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """Set cassettes path."""
    return os.path.join("tests", "cassettes", request.module.__name__.split(".")[-1])


@pytest.mark.clients
@pytest.mark.parametrize("case", cases)
@pytest.mark.vcr()
def test_requests_exceptions(case):
    """Request exceptions tests."""
    with pytest.raises(case[2]) as exc:
        getattr(clients, case[0]).get(case[1], {}, timeout=timeouts[case[0]])
    if isinstance(exc.value, exceptions.ClientHTTPError):
        assert exc.value.code == case[3]  # noqa


@pytest.mark.clients
@pytest.mark.parametrize("client", modules)
@pytest.mark.vcr()
def test_response_csv(client):
    """Request CSV response test."""
    result = getattr(clients, client).get(
        "https://eodhistoricaldata.com/api/eod/MCD.US",
        {"api_token": "demo", "from": "2017-01-05", "to": "2017-01-06", "fmt": "csv"}
    )
    assert result[0] == "text/html"
    assert isinstance(result[1], bytes)


@pytest.mark.clients
@pytest.mark.parametrize("client", modules)
@pytest.mark.vcr()
def test_response_json(client):
    """Request JSON response test."""
    result = getattr(clients, client).get(
        "https://eodhistoricaldata.com/api/eod/MCD.US",
        {"api_token": "demo", "from": "2017-01-05", "to": "2017-01-06", "fmt": "json"}
    )
    assert result[0] == "application/json"
    assert isinstance(result[1], bytes)
