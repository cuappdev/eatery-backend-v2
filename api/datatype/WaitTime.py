class WaitTime:
    def __init__(
            self,
            end_timestamp: int,
            wait_time_low: float,
            wait_time_expected: float,
            wait_time_high: float,
            relative_density: float
    ):
        self.end_timestamp = end_timestamp
        self.wait_time_low = wait_time_low
        self.wait_time_expected = wait_time_expected
        self.wait_time_high = wait_time_high
        self.relative_density = relative_density

    def to_json(self):
        return {
            "block_end_timestamp": self.end_timestamp,
            "block_duration": 5 * 60 * 60,
            "wait_time_low": self.wait_time_low,
            "wait_time_expected": self.wait_time_expected,
            "wait_time_high": self.wait_time_high,
            "relative_density": self.relative_density,
        }
    
