import abc

from gilito import LogBook


class Exporter:
    @abc.abstractmethod
    def process(self, logbook: LogBook) -> bytes:
        raise NotImplementedError()
