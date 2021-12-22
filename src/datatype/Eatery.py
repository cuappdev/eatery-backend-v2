from datetime import date
from typing import Optional


class Eatery:

    def __init__(
            self,
            name: str
    ):
        self.name = name

    def to_json(self, start: Optional[date] = None, end: Optional[date] = None):
        raise Exception()
