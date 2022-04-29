import abc
import datetime
from typing import Any, Callable, Dict, List

from gilito.models import Transaction


class Mapper:
    @abc.abstractmethod
    def map(self, rows: List[Dict[str, str]]) -> List[Transaction]:
        raise NotImplementedError()


def map_to_native_types(
    *, fns: Dict[str, Callable], item: Dict[str, str]
) -> Dict[str, Any]:
    ret = {}

    for (k, v) in item.items():
        try:
            fn = fns[k]
        except KeyError:
            ret[k] = v
        else:
            ret[k] = fn(v)

    return ret


def as_float(value):
    if isinstance(value, float):
        return value

    return float(value.replace(",", "."))


def as_datetime(value, fmt):
    if isinstance(value, datetime.datetime):
        return value
    return datetime.datetime.strptime(value, "%d/%m/%Y")


def as_currency(value):
    iso_4217 = {"€": "EUR"}
    if value not in iso_4217:
        return value

    return iso_4217[value]
