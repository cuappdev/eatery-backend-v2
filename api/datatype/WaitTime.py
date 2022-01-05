class WaitTime:
    def __init__(
            self,
            timestamp: int,
            wait_time_low: float,
            wait_time_expected: float,
            wait_time_high: float
    ):
        self.timestamp = timestamp
        self.wait_time_low = wait_time_low
        self.wait_time_expected = wait_time_expected
        self.wait_time_high = wait_time_high

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "wait_time_low": self.wait_time_low,
            "wait_time_expected": self.wait_time_expected,
            "wait_time_high": self.wait_time_high
        }

    @staticmethod
    def from_json(wait_time_json):
        return WaitTime(
            timestamp = wait_time_json["timestamp"],
            wait_time_low=wait_time_json["wait_time_low"],
            wait_time_expected=wait_time_json["wait_time_expected"],
            wait_time_high=wait_time_json["wait_time_high"]
        )
    
