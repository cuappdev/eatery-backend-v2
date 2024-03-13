from category.models import Category
from category.serializers import CategorySerializer
from item.models import Item

"""
Add categories to Category Model from CornellDiningNow. 

CornellDiningNow models cafe and dining hall categories differently, so they are parsed differently.
"""


class PopulateCategoryController:
    def __init__(self):
        self = self

    def generate_dining_hall_categories(self, json_event, event):
        """
        category_items = {"category_name" : id, ... }
        """
        category_items = {}

        category_order = ["Chef's Table", "Chef's Table - Sides", "Grill", "Wok", 
         "Wok/Asian Station", "Iron Grill", "Mexican Station", "Global",
         "Halal", "Kosher Station", "Flat Top Grill"]
        
        def sort_menu(menu):
            return category_order.index(menu["category"].strip()) if menu["category"].strip() in category_order else len(category_order)

        for json_menu in sorted(json_event["menu"], key=sort_menu):
            data = {"event": event, "category": json_menu["category"]}
            category = CategorySerializer(data=data)

            if category.is_valid():
                category.save()
            else:
                print(category.errors)

            category_name = category.data["category"]
            category_id = category.data["id"]
            category_items[category_name] = category_id

        return category_items

    def generate_cafe_categories(self, json_eatery, event):
        """
        category_items = {"category_name" : id, ... }
        """
        category_items = {}
        categories = []
        dining_items = json_eatery["diningItems"]

        for item in dining_items:
            if item["category"] not in categories:
                categories.append(item["category"])
                data = {"event": event, "category": item["category"]}
                category = CategorySerializer(data=data)
                if category.is_valid():
                    category.save()
                else:
                    print(category.errors)

                category_name = category.data["category"]
                category_id = category.data["id"]
                category_items[category_name] = category_id

        return category_items

    def process(self, events_dict, json_eateries):
        """categories_dict = { eatery_id :
            { event[i] : {"category_name" : id, "category_name" : id},
              event[i] : {"category_name" : id}
            }
        }"""

        categories_dict = {}

        for json_eatery in json_eateries:
            eatery_id = int(json_eatery["id"])
            categories_dict[eatery_id] = {}

            if eatery_id in events_dict:
                eatery_events = events_dict[eatery_id]
                i = 0
            else:
                continue

            is_cafe = "Cafe" in {
                eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
            }
            
            """
            For every event in an eatery --> for every menu in an eatery --> get categories
            """
            json_dates = json_eatery["operatingHours"]
            for json_date in json_dates:
                json_events = json_date["events"]
                for json_event in json_events:
                    if i < len(eatery_events):
                        event = eatery_events[i]
                        i += 1
                        categories_dict[eatery_id][event] = {}

                        if is_cafe:
                            categories = self.generate_cafe_categories(
                                json_eatery, event
                            )
                        else:
                            categories = self.generate_dining_hall_categories(
                                json_event, event
                            )

                        categories_dict[eatery_id][event] = categories

        return categories_dict
