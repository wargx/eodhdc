# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,too-many-arguments
from typing import Union
import pandas as pd
from eodhdc.base import BaseGroup


class AlternativeGroup(BaseGroup):

    """Alternative Data Financial API group.
    https://eodhistoricaldata.com/financial-apis/category/alternative-data-financial-api/
    """

    def sentiment(
        self, source: str, lookup: str, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Financial News Sentiment Data API / Tweets Sentiment Data API.

        :param source: media source, "news" ot "tweets".
        :param lookup: search query, like s=btc-usd.cc,aapl.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        prefix = "sentiments" if source == "news" else "tweets-sentiments"
        response = self.get(
            f"{self.base}/{prefix}",
            self.prepare(locals(), ["source", "prefix"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def events(
        self, country: str = None, comparison: str = None,
        limit: int = 50, offset: int = 0, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Economic Events Data API.

        :param country: country code is in ISO 3166 format.
        :param comparison: one of "mom", "qoq", "yoy".
        :param limit: number of results to be returned, 0 - 1000.
        :param offset: offset of the data, 0 - 1000.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/economic-events",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def news(
        self, symbol: str = None, tag: str = None, limit: int = 50,
        offset: int = 0, start: str = None, finish: str = None,
        args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Stock Market and Financial News API.
        List of supported tags:
        https://eodhistoricaldata.com/financial-apis/stock-market-financial-news-api/

        :param symbol: ticker code to get news for.
        :param tag: tag to get news on a given topic.
        :param limit: number of results to be returned, 0 - 1000.
        :param offset: offset of the data, 0 - 1000.
        :param start: period start date, "YYYY-MM-DD".
        :param finish: period end date, "YYYY-MM-DD".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/news",
            self.prepare(locals(), []), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def macroindicators(
        self, country: str, indicator: str = None,
        fmt: str = "json", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Macro Indicators API.
        List of supported macro indicators:
        https://eodhistoricaldata.com/financial-apis/macroeconomics-data-and-macro-indicators-api/

        :param country: country in the Alpha-3 ISO format.
        :param indicator: macroeconomics data indicator.
        :param fmt: response output format, "csv" or "json".
        :param args: additional / override client arguments.
        :param output: output format for 'process' method.
        :param writer: pandas writer parameters.
        :return: data in requested output format.
        """
        response = self.get(
            f"{self.base}/macro-indicator/{country}",
            self.prepare(locals(), ["country"]), **{**self.args, **(args or {})}
        )
        return self.process(response, output, writer)

    def macroeconomic(
        self, ticker: str, period: str = "d", order: str = "a", start: str = None, finish: str = None,
        extract: str = None, fmt: str = "csv", args: dict = None, output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """End-Of-Day Historical Stock Market Data API.
        A lot more information:
        https://eodhistoricaldata.com/financial-apis/macroeconomic-data-api/

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
