

from .WaitTime import WaitTime

class WaitTimesByDay:
    def __init__(
            self,
            canonical_date: str,
            wait_times: list[WaitTime]
    ):
        self.canonical_date = canonical_date
        self.wait_times = wait_times

    def to_json(self):
        return {
            "canonical_date": self.canonical_date,
            "wait_times": [wait_time.to_json() for wait_time in self.wait_times]
        }
    
