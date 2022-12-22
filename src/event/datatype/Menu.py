from datatype.MenuCategory import MenuCategory

class Menu:

    def __init__(self, categories: list[MenuCategory]):
        self.categories = categories

    def to_json(self):
        return [category.to_json() for category in self.categories]

    @staticmethod
    def from_json(menu_json):
        return Menu(
            categories=[MenuCategory.from_json(category) for category in menu_json]
        )
