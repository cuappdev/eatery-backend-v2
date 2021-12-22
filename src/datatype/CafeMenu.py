from src.datatype.MenuItem import MenuItem


class CafeMenu:

    def __init__(self, items: list[MenuItem]):
        self.items = items

    def to_json(self):
        return [item.to_json() for item in self.items]
