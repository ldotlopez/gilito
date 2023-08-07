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


import csv
import io
import typing

from gilito import LogBook, Transaction
from gilito.plugins import Dumper
from gilito.helpers.csv import load_csv


class Plugin(Dumper):
    def load(self, buffer: bytes):
        return load_csv(buffer)

    def dump(self, logbook: LogBook) -> bytes:
        def transactions_as_dict(x):
            ret = x.dict()
            ret["amount"] = str(x.amount).replace(".", ",")
            ret["date"] = x.date.strftime("%d/%m/%Y")
            if x.category:
                ret["category"] = x.category.name

            ret["tags"] = ",".join(x.tags)

            return ret

        fh = io.StringIO()

        headers = list(typing.get_type_hints(Transaction).keys())
        headers.remove("date")
        headers = ["date"] + headers
        writter = csv.DictWriter(fh, fieldnames=headers)
        writter.writeheader()
        writter.writerows([transactions_as_dict(x) for x in logbook.transactions])

        fh.seek(0)
        return fh.read().encode("utf-8")
