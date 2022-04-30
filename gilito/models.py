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
