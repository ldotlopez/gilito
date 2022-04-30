import abc
from typing import Callable, List

from gilito import LogBook, Transaction


class Processor:
    def process(self, logbook: LogBook):
        return LogBook(
            transactions=[self.process_one(item) for item in logbook.transactions]
        )

    @abc.abstractmethod
    def process_one(self, item: Transaction) -> Transaction:
        raise NotImplementedError()


class Filter:
    @abc.abstractmethod
    def matches(self, transaction: Transaction) -> bool:
        raise NotImplementedError()


class Or(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def matches(self, transaction: Transaction) -> bool:
        for f in self.filters:
            if f.matches(transaction):
                return True

        return False


class And(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def matches(self, transaction: Transaction) -> bool:
        return all([f.matches(transaction) for f in self.filters])


class TextFieldComparable:
    def __init__(self, field: str, needle: str, *, ignore_case=True):
        self.field = field
        self.needle = needle
        self.ignore_case = ignore_case

    def custom_match(self, transaction: Transaction, fn: Callable) -> bool:
        haystack = getattr(transaction, self.field, "")
        haystack = str(haystack)

        if self.ignore_case:
            haystack = haystack.lower()
            needle = self.needle.lower()

        return fn(haystack, needle)


class TextFieldContains(Filter, TextFieldComparable):
    def matches(self, transaction: Transaction) -> bool:
        return self.custom_match(
            transaction, lambda haystack, needle: needle in haystack
        )


class TextFieldEquals(TextFieldComparable):
    def matches(self, transaction: Transaction) -> bool:
        return self.custom_match(
            transaction, lambda haystack, needle: needle == haystack
        )


class Contains(Or):
    TEXT_FIELDS = ["description", "notes"]

    def __init__(self, needle: str, *, ignore_case=True):
        super().__init__(
            filters=[TextFieldContains(field, needle) for field in self.TEXT_FIELDS]
        )
