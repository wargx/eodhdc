# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
from typing import Union
from types import ModuleType
import asyncio
import importlib
from eodhdc import groups, exceptions


class EODHDClient:
    """EODHD HTTP client class"""

    def __init__(self, client: Union[str, ModuleType], key: str = "demo", args: dict = None):
        """
        :param client: client name or module.
        :param key: api token.
        :param args: common client arguments.
        """
        self.mode = "sync"
        self.key = key
        self.args = args or {}
        self.session = None

        if isinstance(client, str):
            try:
                self.client = importlib.import_module(f"eodhdc.clients.{client}")
            except ImportError:
                raise exceptions.UnknownClient(f"Unknown client '{client}'") from None
        else:
            self.client = client

        if not getattr(self.client, "get", None):
            raise exceptions.ImproperClient(f"Client '{client}' doesn't have <get> method")
        if asyncio.iscoroutinefunction(self.client.get):
            self.mode = "coro"
        if self.mode == "coro" and hasattr(self.client, "create"):
            self.session = self.client.create()

        if self.mode == "coro":
            self.alternative = groups.coro.AlternativeGroup(self.client.get, key, self.session, self.args)
            self.exchange = groups.coro.ExchangeGroup(self.client.get, key, self.session, self.args)
            self.fundamental = groups.coro.FundamentalGroup(self.client.get, key, self.session, self.args)
            self.market = groups.coro.MarketGroup(self.client.get, key, self.session, self.args)
        else:
            self.alternative = groups.sync.AlternativeGroup(self.client.get, key, self.session, self.args)
            self.exchange = groups.sync.ExchangeGroup(self.client.get, key, self.session, self.args)
            self.fundamental = groups.sync.FundamentalGroup(self.client.get, key, self.session, self.args)
            self.market = groups.sync.MarketGroup(self.client.get, key, self.session, self.args)

    async def destroy(self):
        """Manually close client session."""
        if self.session and hasattr(self.client, "destroy"):
            await self.client.destroy(self.session)
