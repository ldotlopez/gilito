import csv
import io
import typing

from gilito import LogBook, Transaction
from gilito.plugins import Dumper


class Plugin(Dumper):
    def dump(self, logbook: LogBook) -> bytes:
        def transactions_as_dict(x):
            ret = x.dict()
            if x.category:
                ret["category"] = x.category.name
            if x.tags:
                ret["tags"] = ",".join(x.tags)

            return ret

        fh = io.StringIO()

        headers = typing.get_type_hints(Transaction).keys()
        writter = csv.DictWriter(fh, fieldnames=headers)
        writter.writeheader()
        writter.writerows([transactions_as_dict(x) for x in logbook.transactions])

        fh.seek(0)
        return fh.read().encode("utf-8")
