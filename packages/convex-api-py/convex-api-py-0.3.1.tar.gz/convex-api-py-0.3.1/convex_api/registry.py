"""

    ConvexRegistry

"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    cast
)

if TYPE_CHECKING:
    from convex_api.api import API

import logging

from convex_api.account import Account
from convex_api.exceptions import ConvexAPIError

logger = logging.getLogger(__name__)

QUERY_ACCOUNT_ADDRESS = 9


class Registry:

    def __init__(self, convex: API):
        self._convex = convex
        self._address = None
        self._items: dict[str, tuple[int, int] | None] = {}

    def is_registered(self, name: str):
        return self.item(name) is not None

    def item(self, name: str):
        if name not in self._items:
            result = self._convex.query(f'(get cns-database (symbol "{name}"))', self.address)
            logger.debug(f'cns-database: {result}')
            self._items[name] = None
            if isinstance(result.value, (list, tuple)):
                self._items[name] = cast(tuple[int, int], result.value)
        return self._items[name]

    def clear(self):
        self._items = {}
        self._address = None

    def register(self, name: str, contract_address: int, account: Account):
        result = self._convex.send(f'(call #{self.address} (register {{:name (symbol "{name}")}}))', account)
        logger.debug(f'register result: {result}')
        if result and hasattr(result, 'value'):
            try:
                result = self._convex.send(f'(call #{self.address} (cns-update (symbol "{name}") #{contract_address}))', account)
                logger.debug(f'cns-update result: {result}')
                if result and hasattr(result, 'value'):
                    items = result.value
                    if name in items:
                        item: tuple[int, int] = items[name]
                        self._items[name] = item
                        return item
            except ConvexAPIError as e:
                logger.debug(f'convex error: {e}')
                raise

    def resolve_owner(self, name: str) -> int | None:
        item = self.item(name)
        if item:
            return item[1]

    def resolve_address(self, name: str) -> int | None:
        item = self.item(name)
        if item:
            return item[0]

    @property
    def address(self) -> int:
        if self._address is None:
            result = self._convex.query('(address *registry*)', QUERY_ACCOUNT_ADDRESS)
            self._registry_address = Account.to_address(result.value)
            logger.debug(f'registry_address: {self._registry_address}')
        return self._registry_address
