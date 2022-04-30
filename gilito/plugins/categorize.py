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


from gilito.models import Category, Transaction
from gilito.plugins import Processor


class Plugin(Processor):
    def __init__(self, *args, processing_rules=None, **kwargs):
        self.processing_rules = processing_rules or []
        super().__init__(*args, **kwargs)

    def process_one(self, transaction: Transaction) -> Transaction:
        for (category, f) in self.processing_rules:
            if f.matches(transaction):
                transaction.category = Category(name=category)

        return transaction
