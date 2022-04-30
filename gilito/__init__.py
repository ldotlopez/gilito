import enum
import importlib
from typing import List, Dict, List, TypeVar, Generic
from datetime import datetime

from .models import Transaction

# def factory(basecls, *args, **kwargs):
#     for x in basecls.__subclasses__():
#         if x.can_handle(*args, **kwargs):
#             return x
#
#     if basecls.can_handle(*args, **kwargs):
#         return basecls

_LogBookTypeVar = TypeVar("_LogBookTypeVar")


class LogBook(Generic[_LogBookTypeVar]):
    def __init__(self, *, transactions: List[Transaction]):
        self.transactions: List = list(transactions)

    def __iter__(self):
        yield from iter(self.transactions)

    def override(self, overrides: _LogBookTypeVar):
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


def get_plugin(type: PluginType, name: str):
    return importlib.import_module(f"gilito.{type.value}.{name}")


__all__ = ["Transaction", "LogBook", "PluginType"]
