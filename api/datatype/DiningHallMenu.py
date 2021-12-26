from api.datatype.DiningHallMenuCategory import DiningHallMenuCategory


class DiningHallMenu:

    def __init__(self, categories: list[DiningHallMenuCategory]):
        self.categories = categories

    def to_json(self):
        return [category.to_json() for category in self.categories]
