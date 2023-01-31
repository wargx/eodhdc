# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,too-many-arguments
from typing import Union
import pandas as pd
from eodhdc.base import BaseGroup


class ExchangeGroup(BaseGroup):

    """Exchanges (Stock Market) Financial APIs group.
    https://eodhistoricaldata.com/financial-apis/category/exchanges-stock-market-financial-api/
    """

    def bulk(
        self, exchange: str = "US", kind: str = None, date: str = None, symbols: list = None,
        extract: str = None, fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Bulk API for EOD, Splits and Dividends.

        :param exchange: exchange name:
          "US" or "NYSE", "NASDAQ", "BATS", "AMEX".
        :param kind: data type:
          default - "eod" or "splits", "dividends".
        :param date: last day data or for specified date.
        :param symbols: data only for specified tickers.
        :param extract: endpoint specific filter.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/eod-bulk-last-day/{exchange}",
            self.prepare(locals(), ["exchange"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def exchanges(
        self, args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Get List of Exchanges.

        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/exchanges-list/",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def tickers(
        self, exchange: str = "US", delisted: str = "1",
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Get List of Tickers (Exchange Symbols).

        :param exchange: exchange name.
        :param delisted: include inactive tickers.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/exchange-symbol-list/{exchange}",
            self.prepare(locals(), ["exchange"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def details(
        self, exchange: str = "US", start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Historical Splits API.

        :param exchange: exchange name.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/exchange-details/{exchange}",
            self.prepare(locals(), ["exchange"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def history(
        self, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Symbol Change History.

        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/symbol-change-history",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def screener(
        self, filters: str = None, signals: str = None, sort: str = None, limit: int = 50, offset: int = 0,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Stock Market Screener API.

        :param filters: filters out tickers by different fields.
          filters=[[“field1”, “operation1”, value1],[“field2”, “operation2”, value2] , … ]
        :param signals: filter out tickers by signals.
          signals=signal1,signal2,…,signalN
        :param sort: sorts all fields with type 'Number' in asc/desc order.
          sort=field_name.(asc|desc)
        :param limit: number of results to be returned, 1 - 100.
        :param offset: offset of the data, 0 - 1000.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/screener",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def search(
        self, query: str, limit: int = 15, bonds_only: int = 0, exchange: str = None, kind: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Search API for Stocks, ETFs, Mutual Funds and Indices.

        :param query: search query.
        :param limit: number of results to be returned, 1 - 50.
        :param bonds_only: default set or bonds.
        :param exchange: filter output by exchange.
        :param kind: type of asset to search for.
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/search/{query}",
            self.prepare(locals(), ["query"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)
