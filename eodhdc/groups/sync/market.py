# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,too-many-arguments
from typing import Union, List
import pandas as pd
from eodhdc.base import BaseGroup


class MarketGroup(BaseGroup):

    """Stock Market Prices, Splits and Dividends Data API group.
    https://eodhistoricaldata.com/financial-apis/category/historical-prices-live-data-apis/
    """

    def historical(
        self, ticker: str, period: str = "d", order: str = "a", start: str = None, finish: str = None,
        extract: str = None, fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """End-Of-Day Historical Stock Market Data API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param period: "d" - daily, "w" - weekly, "m" - monthly.
        :param order: dates order, "a" - ascending, "d" - descending.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param extract: endpoint specific filter.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/eod/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def delayed(
        self, tickers: List[str], extract: str = None, fmt: str = "csv",
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Live (Delayed) Stock Prices API.

        :param tickers: list of tickers.
        :param extract: endpoint specific filter.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        s = tickers[1:]  # pylint: disable=invalid-name,possibly-unused-variable
        response = self.get(
            f"{self.base}/real-time/{tickers[0]}",
            self.prepare(locals(), ["tickers"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def dividends(
        self, ticker: str, start: str = None, finish: str = None,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Historical Dividends API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/div/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def splits(
        self, ticker: str, start: str = None, finish: str = None,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Historical Splits API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/splits/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def indicators(
        self, ticker: str, function: str, params: dict = None, order: str = "a",
        splitadjusted_only: str = None, start: str = None, finish: str = None,
        extract: str = None, fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Technical Indicator API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param function: technical indicator function.
        :param params: technical indicator function parameters.
        :param order: dates order, "a" - ascending, "d" - descending.
        :param splitadjusted_only: closed adjusted only with splits.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param extract: endpoint specific filter.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/technical/{ticker}",
            self.prepare({**locals(), **(params or {})}, ["ticker", "params"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def intraday(
        self, ticker: str, interval: str = "1m", start: int = None, finish: int = None,
        fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Intraday Historical Data API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param interval: "5m" - 5 minutes, "1h" - 1 hour, "1m" - 1 minute.
        :param start: period start date, UNIX time with UTC timezone, "1564752900".
        :param finish: period end date, UNIX time with UTC timezone, "1564753200".
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/intraday/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def options(
        self, ticker: str, start: str = None, finish: str = None,
        contract: str = None, trade_date_start: str = None, trade_date_finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Options Data API.

        :param ticker: ticker in form {symbol-name}.{exchange-id}.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param contract: contract name.
        :param trade_date_start: last trade period start date, "YYYY-MM-DD".
        :param trade_date_finish: last trade period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/options/{ticker}",
            self.prepare(locals(), ["ticker"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)
