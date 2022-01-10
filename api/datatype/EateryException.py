class EateryException:

    def __init__(
        self, 
        id: int,
        description: str,
        start_timestamp: int,
        end_timestamp: int
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
            "end_timestamp": self.end_timestamp
        }

    @staticmethod
    def from_json(exception_json):
        return EateryException(
            id = exception_json["id"],
            description=exception_json["description"],
            start_timestamp=exception_json["start_timestamp"],
            end_timestamp=exception_json["end_timestamp"]
        )
