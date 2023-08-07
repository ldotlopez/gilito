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


import abc
from typing import Any, Dict, List
from collections.abc import Callable

from gilito import LogBook, Transaction, UnmappedData


class BasePlugin:
    pass


class Loader(BasePlugin):
    @abc.abstractclassmethod
    def can_load_file(cls, filename: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, buffer: bytes) -> UnmappedData:
        raise NotImplementedError


class Mapper(BasePlugin):
    @abc.abstractmethod
    def map(self, data: UnmappedData) -> list[Transaction]:
        raise NotImplementedError()

    @staticmethod
    def map_to_native_types(
        *, fns: dict[str, Callable], item: dict[str, str]
    ) -> dict[str, Any]:
        ret = {}

        for (k, v) in item.items():
            try:
                fn = fns[k]
            except KeyError:
                ret[k] = v
            else:
                ret[k] = fn(v)

        return ret


class Processor(BasePlugin):
    def process(self, logbook: LogBook):
        return LogBook(
            transactions=[self.process_one(item) for item in logbook.transactions]
        )

    @abc.abstractmethod
    def process_one(self, item: Transaction) -> Transaction:
        raise NotImplementedError()


class Dumper:
    @abc.abstractmethod
    def dump(self, logbook: LogBook) -> bytes:
        raise NotImplementedError()
