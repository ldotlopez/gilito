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


import unittest
from gilito import LogBook, Transaction

from datetime import datetime


BASE_TRANSACTIONS = [
    Transaction(amount=1, date=datetime(2022, 1, 1), description="tr #1.1"),
    Transaction(amount=2, date=datetime(2022, 2, 1), description="tr #1.2"),
    Transaction(amount=3, date=datetime(2022, 3, 1), description="tr #1.3"),
]

SET_A = [
    # Matches base #1
    Transaction(amount=1, date=datetime(2022, 1, 1), description="tr #2.1"),
    # Just after base #2
    Transaction(amount=2, date=datetime(2022, 2, 2), description="tr #2.2"),
    # Before base #3
    Transaction(amount=3, date=datetime(2022, 2, 5), description="tr #2.3"),
]


class TestMerge(unittest.TestCase):
    def test_merge(self):
        book = LogBook(transactions=list(BASE_TRANSACTIONS))
        book.merge(LogBook(transactions=list(SET_A)))

        self.assertEqual(
            [x.description for x in book.transactions],
            ["tr #1.1", "tr #2.1", "tr #1.2", "tr #2.2", "tr #2.3", "tr #1.3"],
        )


if __name__ == "__main__":
    unittest.main()
