# -*- coding: utf-8 -*-
import os
import pytest
from eodhdc import EODHDClient

cases = [
    ["crypto", dict(ticker="BTC-USD.CC")],
    ["capitalization", "AAPL.US", dict(start="2023-01-01", finish="2023-01-20")],
    ["insider", "AAPL.US", dict(start="2021-05-01", finish="2021-05-31")],
    ["fundamentals", "AAPL.US", dict(extract="General")],
    ["bulk", "NASDAQ", dict(symbols=["AAPL.US"], limit=10, fmt="json")],
    ["bulk", "NASDAQ", dict(symbols=["AAPL.US"], limit=10, fmt="csv")],
    ["calendar", "trends", dict(symbols=["AAPL.US"], fmt="json")],
    ["calendar", "trends", dict(symbols=["AAPL.US"], fmt="csv")],
    ["calendar", "earnings", dict(symbols=["AAPL.US"], fmt="json")],
    ["calendar", "ipos", dict(symbols=["AAPL.US"], fmt="json")],
    ["calendar", "splits", dict(symbols=["AAPL.US"], fmt="json")],
    ["bonds", dict(code="910047AG4")]
]


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """Set cassettes path."""
    return os.path.join("tests", "cassettes", request.module.__name__.split(".")[-1])


@pytest.mark.groups
@pytest.mark.parametrize("case", cases)
@pytest.mark.vcr()
def test_groups(case):
    """Group sync mode tests."""
    eodhd = EODHDClient("httpxs")
    if len(case) == 2:
        result = getattr(eodhd.fundamental, case[0])(**case[1])
        assert result
    if len(case) == 3:
        result = getattr(eodhd.fundamental, case[0])(case[1], **case[2])
        assert result


@pytest.mark.asyncio
@pytest.mark.groups
@pytest.mark.parametrize("case", cases)
@pytest.mark.vcr()
async def test_groups_async(case):
    """Group async mode tests."""
    eodhd = EODHDClient("httpxa")
    async with eodhd.session:
        if len(case) == 2:
            result = await getattr(eodhd.fundamental, case[0])(**case[1])
            assert result
        if len(case) == 3:
            result = await getattr(eodhd.fundamental, case[0])(case[1], **case[2])
            assert result
