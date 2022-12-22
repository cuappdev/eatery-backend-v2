from typing import Optional

from api.datatype.MenuItemSection import MenuItemSection

class MenuItem:

    def __init__(
            self,
            name: str,
            healthy: Optional[bool] = None,
            base_price: Optional[float] = None,
            description: Optional[str] = None,
            sections: Optional[MenuItemSection] = None
    ):
        self.healthy = healthy
        self.name = name
        self.base_price = base_price
        self.description = description
        self.sections = sections

    def to_json(self):
        return {
            "healthy": self.healthy,
            "name": self.name,
            "base_price": self.base_price,
            "description": self.description,
            "sections": None if self.sections is None else [section.to_json() for section in self.sections]
        }

    @staticmethod
    def from_json(item_json):
        return MenuItem(
            name=item_json["name"],
            healthy=item_json["healthy"],
            base_price=item_json["base_price"],
            description=item_json["description"],
            sections=None if "sections" not in item_json or item_json["sections"] is None
            else [MenuItemSection.from_json(section) for section in item_json["sections"]]
         )
