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
from typing import Any, Dict, List, NewType, Optional

import pydantic

ValidationError = pydantic.ValidationError


class Category(pydantic.BaseModel):
    name: str


class Tag(pydantic.BaseModel):
    name: str


class Transaction(pydantic.BaseModel):
    amount: float
    date: datetime.datetime
    description: str

    notes: str | None = ""
    origin: str | None
    destination: str | None
    category: Category | None
    tags: list[Tag] = []
    currency: str | None

    def __eq__(self, other):
        return self.dict() == other.dict()

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} {self.amount} € ({self.description})"


UnmappedData = NewType("UnmappedData", list[dict[str, Any]])
