class EateryAlert:
    def __init__(
        self, id: int, description: str, start_timestamp: int, end_timestamp: int
    ):
        self.id = id
        self.description = description
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def to_json(self):
        return {
            "id": 1,
            "description": self.description,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
        }

    @staticmethod
    def from_json(alert_json):
        return EateryAlert(
            id=alert_json["id"],
            description=alert_json["description"],
            start_timestamp=alert_json["start_timestamp"],
            end_timestamp=alert_json["end_timestamp"],
        )
