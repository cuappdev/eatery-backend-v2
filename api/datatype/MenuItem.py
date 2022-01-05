class MenuItem:

    @staticmethod
    def from_cornell_dining_json(json_item: dict):
        return MenuItem(
            healthy=json_item["healthy"],
            name=json_item["item"]
        )

    def __init__(
            self,
            healthy: bool,
            name: str
    ):
        self.healthy = healthy
        self.name = name

    def to_json(self):
        return {
            "healthy": self.healthy,
            "name": self.name
        }
    
    @staticmethod
    def from_json(item_json):
        return MenuItem(
            healthy=item_json["healthy"],
            name=item_json["name"]
        )
