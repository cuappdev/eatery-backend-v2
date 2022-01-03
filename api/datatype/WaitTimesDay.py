

from .WaitTime import WaitTime

class WaitTimesDay:
    def __init__(
            self,
            canonical_date: str,
            data: list[WaitTime]
    ):
        self.canonical_date = canonical_date
        self.data = data

    def to_json(self):
        return {
            "canonical_date": self.canonical_date,
            "data": [wait_time.to_json() for wait_time in self.data]
        }
    
