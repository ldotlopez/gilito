import abc
from typing import Any, Callable, Dict, List

from gilito import LogBook, Transaction


class Plugin:
    pass


class Loader(Plugin):
    @abc.abstractclassmethod
    def can_load_file(cls, filename: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, buffer: bytes) -> str:
        raise NotImplementedError


class Mapper(Plugin):
    @abc.abstractmethod
    def map(self, rows: List[Dict[str, str]]) -> LogBook:
        raise NotImplementedError()

    @staticmethod
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


class Processor(Plugin):
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
