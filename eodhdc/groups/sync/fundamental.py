# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,too-many-arguments
from typing import Union, List
import pandas as pd
from eodhdc.base import BaseGroup


class FundamentalGroup(BaseGroup):

    """Fundamental and Economic Financial Data API group.
    https://eodhistoricaldata.com/financial-apis/category/fundamental-and-economic-financial-data-api/
    """

    def crypto(
        self, ticker: str,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Fundamental Data for Cryptocurrencies.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/fundamentals/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def capitalization(
        self, ticker: str, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Historical Market Capitalization API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/historical-market-cap/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def insider(
        self, code: str = None, limit: int = 100, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Insider Transactions API.

        :param code: filter by ticker code.
        :param limit: number of results to be returned, 1 - 1000.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/insider-transactions",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def fundamentals(
        self, ticker: str, extract: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Fundamental Data: Stocks, ETFs, Mutual Funds, Indices.
        A lot more information:
        https://eodhistoricaldata.com/financial-apis/stock-etfs-fundamental-data-feeds/

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param extract: endpoint specific filter.
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/fundamentals/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def bulk(
        self, exchange: str, symbols: List[str] = None, limit: int = 50, offset: int = 0,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Bulk Fundamentals API.

        :param exchange: ticker in form {symbol-name}.{exchange-id}.
        :param symbols: get data only for specific symbols.
        :param limit: number of results to be returned, 1 - 100.
        :param offset: offset of the data, 0 - 1000.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/bulk-fundamentals/{exchange}",
            self.prepare(locals(), ["exchange"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    # pylint: disable=duplicate-code
    def calendar(
        self, kind: str, symbols: List[str] = None, start: int = None, finish: int = None,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Calendar. Upcoming Earnings, Trends, IPOs and Splits.
        Supported parameters by each type:
        https://eodhistoricaldata.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits/

        :param kind: calendar type: "earnings", "trends", "ipos", "splits".
        :param symbols: get data for specified symbols.
        :param start: period start date, UNIX time with UTC timezone, "1564752900".
        :param finish: period end date, UNIX time with UTC timezone, "1564753200".
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        params = {}
        if kind == "earnings":
            params = self.prepare(locals(), ["kind"])
        if kind == "trends":
            params = self.prepare(locals(), ["kind", "start", "finish"])
        if kind == "ipos":
            params = self.prepare(locals(), ["kind", "symbols"])
        if kind == "splits":
            params = self.prepare(locals(), ["kind", "symbols"])
        response = self.get(
            f"{self.base}/calendar/{kind}",
            params, **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def bonds(
        self, code: str,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Bonds Fundamentals API.
        Bonds historical data available in market.historical method
        by using {code}.BOND as ticker.

        :param code: code of a particular bond.
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/bond-fundamentals/{code}",
            self.prepare(locals(), ["code"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)
