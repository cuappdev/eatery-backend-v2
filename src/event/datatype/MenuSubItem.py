from typing import Optional


class MenuSubItem:
    def __init__(
        self, name: str, total_price: Optional[float], additional_price: Optional[float]
    ):
        self.name = name
        self.total_price = total_price
        self.additional_price = additional_price

    def to_json(self):
        return {
            "name": self.name,
            "total_price": self.total_price,
            "additional_price": self.additional_price,
        }

    @staticmethod
    def from_json(item_json):
        return MenuSubItem(
            name=item_json["name"],
            total_price=item_json.get("total_price"),
            additional_price=item_json.get("additional_price"),
        )
