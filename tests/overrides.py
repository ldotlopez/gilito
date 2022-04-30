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
    Transaction(amount=1, date=datetime(2022, 1, 1), description="tr #1"),
    Transaction(amount=2, date=datetime(2022, 1, 2), description="tr #2"),
    Transaction(amount=3, date=datetime(2022, 1, 3), description="tr #3"),
]

ONE_ONE_OVERRIDES = [
    Transaction(amount=2, date=datetime(2022, 1, 2), description="tr #2 fixed"),
]


class TestOverrides(unittest.TestCase):
    def test_just_one(self):
        base = LogBook(transactions=list(BASE_TRANSACTIONS))
        overrides = LogBook(transactions=list(ONE_ONE_OVERRIDES))

        base.override(overrides=overrides)

        self.assertEqual(base.transactions[1], ONE_ONE_OVERRIDES[0])


if __name__ == "__main__":
    unittest.main()
