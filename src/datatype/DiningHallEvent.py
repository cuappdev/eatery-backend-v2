from typing import Optional

from src.datatype.Event import Event
from src.datatype.DiningHallMenu import DiningHallMenu
from datetime import date


class DiningHallEvent(Event):

    def __init__(
            self,
            description: str,
            canonical_date: date,
            start_timestamp: int,
            end_timestamp: int,
            menu: Optional[DiningHallMenu]
    ):
        super().__init__(
            canonical_date=canonical_date,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.description = description
        self.menu = menu

    def to_json(self):
        return {
            "description": self.description,
            "canonical_date": str(self.canonical_date),
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "menu": self.menu.to_json() if self.menu is not None else None
        }
