from api.datatype.MenuItem import MenuItem


class MenuCategory:

    def __init__(self, category: str, items: list[MenuItem]):
        self.category = category
        self.items = items

    def to_json(self):
        return {
            "category": self.category,
            "items": [item.to_json() for item in self.items],
        }

    @staticmethod
    def from_json(category_json):
        return MenuCategory(
            category=category_json["category"],
            items=[MenuItem.from_json(item) for item in category_json["items"]],
        )
