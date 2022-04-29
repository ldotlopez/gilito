import enum
import importlib

from .models import LogBook, Transaction


# def factory(basecls, *args, **kwargs):
#     for x in basecls.__subclasses__():
#         if x.can_handle(*args, **kwargs):
#             return x
#
#     if basecls.can_handle(*args, **kwargs):
#         return basecls


class PluginType(enum.Enum):
    IMPORTER = "importers"
    MAPPER = "mappers"
    PROCESSOR = "processors"
    EXPORTER = "exporters"


def get_plugin(type: PluginType, name: str):
    return importlib.import_module(f"gilito.{type.value}.{name}")


__all__ = ["Transaction", "LogBook", "PluginType"]
