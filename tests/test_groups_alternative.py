# -*- coding: utf-8 -*-
import os
import pytest
from eodhdc import EODHDClient

cases = [
    ["sentiment", "news", dict(lookup="AAPL,TSLA", start="2023-01-01", finish="2023-01-10")],
    ["sentiment", "tweets", dict(lookup="AAPL,TSLA", start="2023-01-01", finish="2023-01-10")],
    ["events", dict(limit=5)],
    ["news", dict(symbol="AAPL.US", limit=5)],
    ["macroindicators", "USA", dict(fmt="json")],
    ["macroindicators", "USA", dict(fmt="csv")],
    ["macroeconomic", "UK10Y.GBOND", dict(start="2023-01-01", finish="2023-01-10", fmt="json")],
    ["macroeconomic", "UK10Y.GBOND", dict(start="2023-01-01", finish="2023-01-10", fmt="csv")]
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
        result = getattr(eodhd.alternative, case[0])(**case[1])
        assert result
    if len(case) == 3:
        result = getattr(eodhd.alternative, case[0])(case[1], **case[2])
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
            result = await getattr(eodhd.alternative, case[0])(**case[1])
            assert result
        if len(case) == 3:
            result = await getattr(eodhd.alternative, case[0])(case[1], **case[2])
            assert result
