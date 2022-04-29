import abc

from gilito.models import LogBook, Transaction


class Processor:
    def process(self, logbook: LogBook):
        return LogBook(
            transactions=[self.process_one(item) for item in logbook.transactions]
        )

    @abc.abstractmethod
    def process_one(self, item: Transaction) -> Transaction:
        raise NotImplementedError()
