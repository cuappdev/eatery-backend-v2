from datetime import date
from typing import Optional

import pytz


class Eatery:

    def __init__(
            self,
            name: str
    ):
        self.name = name

    def to_json(
            self,
            tzinfo: pytz.timezone,
            start: Optional[date] = None,
            end: Optional[date] = None
    ):
        raise Exception()
