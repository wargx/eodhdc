# -*- coding: utf-8 -*-
import os
import pytest
from eodhdc import EODHDClient

cases = [
    ["bulk", "NYSE", dict(symbols=["AAPL"], fmt="json")],
    ["bulk", "NYSE", dict(symbols=["AAPL"], fmt="csv")],
    ["exchanges"],
    ["tickers", "OTC", dict(fmt="json")],
    ["tickers", "OTC", dict(fmt="csv")],
    ["details", "US", dict(start="2023-01-01", finish="2023-12-31")],
    ["history", dict(start="2023-01-01", finish="2023-12-31")],
    [
        "screener",
        '[["market_capitalization",">",1000],["name","match","apple"],["code","=","AAPL"]]',
        dict(sort="market_capitalization.desc", limit=10, offset=0)
    ],
    ["search", dict(query="Apple")]
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
    if len(case) == 1:
        result = getattr(eodhd.exchange, case[0])()
        assert result
    if len(case) == 2:
        result = getattr(eodhd.exchange, case[0])(**case[1])
        assert result
    if len(case) == 3:
        result = getattr(eodhd.exchange, case[0])(case[1], **case[2])
        assert result


@pytest.mark.asyncio
@pytest.mark.groups
@pytest.mark.parametrize("case", cases)
@pytest.mark.vcr()
async def test_groups_async(case):
    """Group async mode tests."""
    eodhd = EODHDClient("httpxa")
    async with eodhd.session:
        if len(case) == 1:
            result = await getattr(eodhd.exchange, case[0])()
            assert result
        if len(case) == 2:
            result = await getattr(eodhd.exchange, case[0])(**case[1])
            assert result
        if len(case) == 3:
            result = await getattr(eodhd.exchange, case[0])(case[1], **case[2])
            assert result
