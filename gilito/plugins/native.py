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


from gilito.plugins import Loader, Dumper, Mapper
import json
from gilito import TabularData, LogBook, Transaction, Category
from gilito.typetools import as_currency, as_datetime, as_float
from gilito.models import ValidationError

FIELD_AMOUNT = "amount"
FIELD_CATEGORY = "category"
FIELD_CURRENCY = "currency"
FIELD_DATE = "date"
FIELD_DESCRIPTION = "description"
FIELD_DESTINATION = "destination"
FIELD_NOTES = "notes"
FIELD_ORIGIN = "origin"
FIELD_TAGS = "tags"


def as_Y_m_d_H_M_S(value):
    return as_datetime(value, "%Y-%m-%d %H:%M:%S")


def as_category(value):
    return Category(name=value)


def as_tags(value):
    # FIXME
    return []


type_conversion_map = {
    FIELD_AMOUNT: as_float,
    FIELD_DATE: as_Y_m_d_H_M_S,
    FIELD_CURRENCY: as_currency,
    FIELD_CATEGORY: as_category,
    FIELD_TAGS: as_tags,
}


class Plugin(Loader, Dumper, Mapper):
    def dump(self, logbook: LogBook) -> bytes:
        def _dict(transaction):

            ret = transaction.dict()
            if transaction.date:
                ret["date"] = str(transaction.date)

            if transaction.category:
                ret["category"] = transaction.category.name

            if transaction.tags:
                ret["tags"] = ",".join(transaction.tags)

            return ret

        return json.dumps(
            {"transactions": [_dict(x) for x in logbook.transactions]}
        ).encode("utf-8")

    def map(self, data: TabularData) -> LogBook:
        def _map_row(row, *, col_idx_map):
            dictrow = {col_idx_map[col_idx]: cell for (col_idx, cell) in enumerate(row)}
            typedrow = self.map_to_native_types(item=dictrow, fns=type_conversion_map)
            return typedrow

        def _transaction_generator(data):
            headers = data[0]
            col_idx_map = dict(enumerate(headers))

            for row in data[1:]:
                if row == []:
                    continue

                mapped_row = _map_row(row, col_idx_map=col_idx_map)
                yield Transaction(**mapped_row)

        return LogBook(transactions=list(_transaction_generator(data)))
