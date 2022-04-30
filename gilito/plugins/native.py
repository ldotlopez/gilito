# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


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
