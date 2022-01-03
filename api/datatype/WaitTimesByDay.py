

from .WaitTime import WaitTime

class WaitTimesByDay:
    def __init__(
            self,
            canonical_date: str,
            daily_wait_times: list[WaitTime]
    ):
        self.canonical_date = canonical_date
        self.daily_wait_times = daily_wait_times

    def to_json(self):
        return {
            "canonical_date": self.canonical_date,
            "daily_wait_times": [wait_time.to_json() for wait_time in self.daily_wait_times]
        }
    
