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
from typing import Generic, List, Optional, TypeVar

from .models import Transaction

# def factory(basecls, *args, **kwargs):
#     for x in basecls.__subclasses__():
#         if x.can_handle(*args, **kwargs):
#             return x
#
#     if basecls.can_handle(*args, **kwargs):
#         return basecls

LogBookT = TypeVar("LogBookT")


class LogBook(Generic[LogBookT]):
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
        def _create_indexed_log(transactions):
            ret = {}

            for tr in transactions:
                if tr.date not in ret:
                    ret[tr.date] = []

                ret[tr.date].append(tr)

            return ret

        ours = _create_indexed_log(self.transactions)
        updated = list(overrides)

        while updated:
            updated_transaction = updated.pop(0)
            try:
                idx = ours[updated_transaction.date].index(updated_transaction)
            except (KeyError, ValueError):
                pass

            raise NotImplementedError(
                "override is tricky: we can't match anything since anything can be "
                "changed"
            )


class PluginType(enum.Enum):
    IMPORTER = "importers"
    MAPPER = "mappers"
    PROCESSOR = "processors"
    EXPORTER = "exporters"
    DUMPER = "dumpers"


def get_plugin(name: str):
    return importlib.import_module(f"gilito.plugins.{name}").Plugin


__all__ = ["Transaction", "LogBook", "PluginType"]
