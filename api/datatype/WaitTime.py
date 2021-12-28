
class WaitTime:
    def __init__(
            self,
            end_timestamp: int,
            wait: float
    ):
        self.end_timestamp = end_timestamp
        self.wait = wait

    def to_json(self):
        return {
            "block_end_timestamp": self.end_timestamp,
            "block_duration": 5 * 60 * 60,
            "wait": self.wait
        }
    
