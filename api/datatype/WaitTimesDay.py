from datetime import date
from .WaitTime import WaitTime


class WaitTimesDay:
    def __init__(
            self,
            canonical_date: date,
            data: list[WaitTime]
    ):
        self.canonical_date = canonical_date
        self.data = data

    def to_json(self):
        return {
            "canonical_date": str(self.canonical_date),
            "data": [wait_time.to_json() for wait_time in self.data]
        }

    @staticmethod
    def from_json(wait_times_day_json):
        return WaitTimesDay(
            canonical_date=date.fromisoformat(wait_times_day_json["canonical_date"]),
            data=[WaitTime.from_json(wait_time) for wait_time in wait_times_day_json["data"]]
        )
