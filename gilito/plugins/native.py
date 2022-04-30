from gilito.plugins import Loader, Dumper, LogBook
import json


class Plugin(Loader, Dumper):
    def load(self, buffer: bytes) -> str:
        return buffer.decode('utf-8')

    def dump(self, logbook: LogBook) -> bytes:
        def _dict(transaction):

            ret = transaction.dict()
            if transaction.date:
                ret['date'] = str(transaction.date)

            if transaction.category:
                ret['category'] = transaction.category.name

            if transaction.tags:
                ret['tags'] = ','.join(transaction.tags)

            return ret

        return json.dumps({
            'transactions': [_dict(x) for x in logbook.transactions]
        }).encode('utf-8')
