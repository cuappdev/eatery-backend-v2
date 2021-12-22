from src.datatype.Event import Event


class CafeEvent(Event):

    def to_json(self):
        return {
            "canonical_date": str(self.canonical_date),
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp
        }
