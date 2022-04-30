# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import enum
import importlib
from typing import Any, Generic, List, NewType, Optional, TypeVar

from .models import Category, Tag, Transaction

# def factory(basecls, *args, **kwargs):
#     for x in basecls.__subclasses__():
#         if x.can_handle(*args, **kwargs):
#             return x
#
#     if basecls.can_handle(*args, **kwargs):
#         return basecls

TabularData = NewType("TabularData", List[List[Any]])

LogBookT = TypeVar("LogBookT")


class LogBook(Generic[LogBookT]):
    TRANSACTION_INDEX_FIELDS = ["amount", "date", "origin", "destination"]
    TRANSACTION_UPDATE_FIELDS = ["description", "notes", "category", "tags"]

    def __init__(self, *, transactions: Optional[List[Transaction]] = None):
        self._transactions: List = list(transactions or [])

    @property
    def transactions(self):
        return self._transactions

    def __iter__(self):
        yield from iter(self.transactions)

    def merge(self, *logbooks: LogBookT):
        logbooks = [self] + list(logbooks)

        transactions = []
        for book_idx, book in enumerate(logbooks):
            for (line, tr) in enumerate(book.transactions):
                transactions.append((tr.date, book_idx, line, tr))

        transactions = sorted(transactions)
        self._transactions = [x[3] for x in transactions]

    def override(self, overrides: LogBookT):
        def _get_transaction_idx_key(tr):
            return tuple(
                [getattr(tr, field) for field in self.TRANSACTION_INDEX_FIELDS]
            )

        def _build_indexed_table(transactions):
            table = {}

            for tr in transactions:
                idx = _get_transaction_idx_key(tr)
                if idx not in table:
                    table[idx] = []

                table[idx].append(tr)

            return table

        def _update_transaction(base, updated):
            for field in self.TRANSACTION_UPDATE_FIELDS:
                setattr(base, field, getattr(updated, field, None))

        ours = _build_indexed_table(self.transactions)
        updated = list(overrides)

        while updated:
            updated_transaction = updated.pop(0)
            updated_idx = _get_transaction_idx_key(updated_transaction)

            if updated_idx not in ours:
                continue

            for tr in ours[updated_idx]:
                ours_idx = _get_transaction_idx_key(tr)
                if ours_idx != updated_idx:
                    continue

                _update_transaction(tr, updated_transaction)
                break


class PluginType(enum.Enum):
    IMPORTER = "importers"
    MAPPER = "mappers"
    PROCESSOR = "processors"
    EXPORTER = "exporters"
    DUMPER = "dumpers"


def get_plugin(name: str):
    return importlib.import_module(f"gilito.plugins.{name}").Plugin


__all__ = ["Transaction", "LogBook", "PluginType", "Category", "Tag"]
