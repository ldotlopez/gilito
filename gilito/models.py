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


import datetime
from typing import List, Optional

import pydantic


class Category(pydantic.BaseModel):
    name: str


class Tag(pydantic.BaseModel):
    name: str


class Transaction(pydantic.BaseModel):
    amount: float
    date: datetime.datetime
    description: str

    notes: Optional[str] = ""
    origin: Optional[str]
    destination: Optional[str]
    category: Optional[Category]
    tags: List[Tag] = []
    currency: Optional[str]

    def __eq__(self, other):
        return self.dict() == other.dict()
