from api.dfg.preparation.datatype.MenuItem import MenuItem

class MenuCategory:

    def __init__(self, category: str, items: list[MenuItem]):
        self.category = category
        self.items = items

    def to_json(self):
        return {
            "category": self.category,
            "items": [item.to_json() for item in self.items]
        }
