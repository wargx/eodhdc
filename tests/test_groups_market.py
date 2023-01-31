# -*- coding: utf-8 -*-
import os
import pytest
from eodhdc import EODHDClient

cases = [
    ["historical", "MCD.US", dict(start="2023-01-01", finish="2023-01-10", fmt="json")],
    ["historical", "MCD.US", dict(start="2023-01-01", finish="2023-01-10", fmt="csv")],
    ["delayed", ["MCD.US", "AAPL.US"], dict(fmt="json")],
    ["delayed", ["MCD.US"], dict(fmt="csv")],
    ["dividends", "MCD.US", dict(start="2022-01-01", finish="2022-12-31", fmt="json")],
    ["dividends", "MCD.US", dict(start="2022-01-01", finish="2022-12-31", fmt="csv")],
    ["splits", "AAPL.US", dict(start="2020-01-01", finish="2022-12-31", fmt="json")],
    ["splits", "AAPL.US", dict(start="2020-01-01", finish="2022-12-31", fmt="csv")],
    ["intraday", "AAPL.US", dict(start=1564752900, finish=1564753200, fmt="json")],
    ["intraday", "AAPL.US", dict(start=1564752900, finish=1564753200, fmt="csv")],
    ["indicators", "AAPL.US", dict(function="stochastic", start="2020-01-01", finish="2020-03-01", fmt="json")],
    ["indicators", "AAPL.US", dict(function="stochastic", start="2020-01-01", finish="2020-03-01", fmt="csv")],
    ["options", "AAPL.US", dict(start="2022-01-01", finish="2022-01-07")]
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
    result = getattr(eodhd.market, case[0])(case[1], **case[2])
    assert result


@pytest.mark.asyncio
@pytest.mark.groups
@pytest.mark.parametrize("case", cases)
@pytest.mark.vcr()
async def test_groups_async(case):
    """Group async mode tests."""
    eodhd = EODHDClient("httpxa")
    async with eodhd.session:
        result = await getattr(eodhd.market, case[0])(case[1], **case[2])
    assert result
