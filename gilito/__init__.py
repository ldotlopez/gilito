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


def get_plugin(type: PluginType, name: str):
    return importlib.import_module(f"gilito.{type.value}.{name}")


__all__ = ["Transaction", "LogBook", "PluginType"]
