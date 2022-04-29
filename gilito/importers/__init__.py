import abc


class Importer:
    @abc.abstractclassmethod
    def can_handle(cls, filename: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self, buffer: bytes) -> str:
        raise NotImplementedError()


class Error(Exception):
    pass
