from api.dfg.preparation.datatype.MenuCategory import MenuCategory

class Menu:

    def __init__(self, categories: list[MenuCategory]):
        self.categories = categories

    def to_json(self):
        return [category.to_json() for category in self.categories]
