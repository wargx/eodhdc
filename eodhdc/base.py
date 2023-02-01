# -*- coding: utf-8 -*-
from typing import Union, Tuple, Any
from typing import Callable, Coroutine
import io
import json
import pathlib
import pandas as pd
from eodhdc import exceptions


class BaseGroup:
    """Base class for groups."""

    def __init__(self, get: Union[Callable, Coroutine], key: str = "demo",
                 session: Any = None, args: dict = None):
        """
        :param get: client <get> function.
        :param key: api token.
        :param session: client session.
        :param args: common client arguments.
        """
        self.get = get
        self.key = key
        self.session = session
        self.args = args or {}
        self.base = "https://eodhistoricaldata.com/api"

    def prepare(self, source: dict, exclude: list) -> dict:
        """Prepare parameters dictionary.

        :param source: source dictionary.
        :param exclude: list of keys to exclude.
        :return: processed parameters.
        """
        result = {
            "api_token": self.key
        }
        convert = {
            "symbol": "s", "start": "from", "finish": "to", "kind": "type",
            "contract": "contract_name", "extract": "filter", "tag": "t", "lookup": "s",
            "trade_date_start": "trade_date_from", "trade_date_finish": "trade_date_to"
        }
        exclude = ["self", "args", "output", "writer"] + exclude
        for key, value in source.items():
            if key in exclude or value is None:
                continue
            result[convert.get(key, key)] = value
        return result

    # pylint: disable=too-many-branches,too-many-statements
    @staticmethod
    def process(
        response: Tuple[str, bytes], output: str = "content", writer: dict = None
    ) -> Union[bytes, dict, str, pd.DataFrame]:
        """Process response data.

        :param response: client response data.
        :param output: output format and optionally file location, format: "<type>[:path]"
            types:

              - "response": raw binary response body
              - "content": decoded as response content type
              - "pandas": pandas dataframe

            path: additionally save response to file

              - for "response" and "content" will save as is
              - for "pandas" will save in format specified by extension:
                parquet, pickle, csv, hdf, xlsx, json, html, feather, tex, dta, md

        :param writer: pandas writer parameters, see original to_<format> methods for more details.
            note that some formats may require 3rd-party libraries.
            additionally writer can be provided with:

              - change:columns - dict to rename DataFrame columns
              - change:reorder - bool to use columns dict for DataFrame columns order
              - change:reindex - str or list to set DataFrame columns as index

        :return: data in requested output format.
        """
        result = None
        output = output.split(":")
        extensions = {
            ".parquet": "parquet", ".pickle": "pickle", ".csv": "csv", ".hdf": "hdf",
            ".xlsx": "excel", ".json": "json", ".html": "html", ".feather": "feather",
            ".tex": "latex", ".dta": "stata", ".md": "markdown"
        }
        if response[0] == "application/csv":
            response = ("text/html", response[1])
        responses = ["application/json", "text/html"]
        if response[0] not in responses:
            raise exceptions.UnsupportedContentType(f"Unsupported content type '{response[0]}'")

        if output[0] == "response":
            result = response[1]

        if output[0] == "content":
            if response[0] == responses[0]:
                try:
                    result = json.loads(response[1])
                except json.JSONDecodeError as ex:
                    raise exceptions.JSONDecodeError(ex, ex.msg)
            if response[0] == responses[1]:
                try:
                    result = response[1].decode("utf-8")
                except UnicodeDecodeError as ex:
                    raise exceptions.BytesDecodeError(ex, str(ex))

        if len(output) == 2 and output[0] in ["response", "content"]:
            try:
                with open(output[1], "wb") as handle:
                    handle.write(response[1])
            except OSError as ex:
                raise exceptions.FileIOError(str(ex)) from None

        if output[0] == "pandas":
            try:
                if response[0] == responses[0]:
                    result = pd.read_json(io.BytesIO(response[1]))
                if response[0] == responses[1]:
                    result = pd.read_csv(io.BytesIO(response[1]))
                if writer:
                    columns = writer.pop("change:columns", None)
                    reorder = writer.pop("change:reorder", None)
                    reindex = writer.pop("change:reindex", None)
                    if columns:
                        result.rename(columns=columns, inplace=True)
                    if reorder:
                        result = result[columns.values()]
                    if reindex:
                        result.set_index(reindex, inplace=True)
                if len(output) == 2:
                    extension = pathlib.Path(output[1]).suffix
                    if pathlib.Path(output[1]).suffix not in extensions:
                        raise exceptions.UnsupportedExtension(f"Unsupported extension '{extension}'")
                    getattr(result, f"to_{extensions[extension]}")(output[1], **(writer or {}))
            except exceptions.UnsupportedExtension:
                raise
            except Exception as ex:
                raise exceptions.PandasRuntimeError(ex, str(ex))

        return result
