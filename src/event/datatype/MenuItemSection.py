from api.datatype.MenuSubItem import MenuSubItem


class MenuItemSection:

    def __init__(self, name: str, subitems: list[MenuSubItem]):
        self.name = name
        self.subitems = subitems

    def to_json(self):
        return {
            "name": self.name,
            "subitems": [item.to_json() for item in self.subitems],
        }

    @staticmethod
    def from_json(section_json):
        return MenuItemSection(
            name=section_json["name"],
            subitems=[MenuSubItem.from_json(item) for item in section_json["subitems"]],
        )
