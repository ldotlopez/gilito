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
