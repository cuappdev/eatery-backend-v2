from category.models import Category
from category.serializers import CategorySerializer
from item.models import Item 

class PopulateCategoryController():
    def __init__(self):
        self = self 

    def generate_dining_hall_categories(self, json_event, menu):
        """
        categories = {"category_name" : id, ... }
        """
        category_items = {}
        for json_menu in json_event['menu']: 
            data = {
                "menu" : int(menu.data['id']),
                "category" : json_menu['category']
            }
            category = CategorySerializer(data=data)

            if category.is_valid():
                category.save()
            else:
                print(category.errors)
            
            category_name = category.data['category']
            category_id = category.data['id']
            category_items[category_name] = category_id

        return category_items

    def generate_cafe_categories(self, json_eatery, menu):
        """
        categories = {"category_name" : id, ... }
        """
        category_items = {}
        categories = []
        dining_items = json_eatery["diningItems"]

        for item in dining_items:
            if item["category"] not in categories:
                categories.append(item["category"])
                data = {
                    "menu" : int(menu.data['id']),
                    "category" : item["category"]
                }
                category = CategorySerializer(data=data)
                if category.is_valid():
                    category.save()
                else:
                    print(category.errors)

                category_name = category.data['category']
                category_id = category.data['id']
                category_items[category_name] = category_id
        
        return category_items
            
    def process(self, menus_dict, json_eateries):
        
        """categories_dict = { eatery_id : 
                    { menu[i] : {"category_name" : id, "category_name" : id}, 
                      menu[i] : {"category_name" : id}
                    }
                }"""
        
        categories_dict = {}

        for json_eatery in json_eateries:
            categories_dict[int(json_eatery["id"])] = {}

            if int(json_eatery["id"]) in menus_dict:
                eatery_menus = menus_dict[int(json_eatery["id"])]; i=0
            else:
                continue

            is_cafe = "Cafe" in {
                eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
            }  

            json_dates = json_eatery["operatingHours"]
            for json_date in json_dates: 
                json_events = json_date["events"]
                for json_event in json_events: 
                    if i < len(eatery_menus):  
                        menu = eatery_menus[i]; i += 1

                        categories_dict[int(json_eatery["id"])][menu.data['id']] = {}

                        if is_cafe: 
                            categories = self.generate_cafe_categories(json_eatery, menu)
                        else: 
                            categories = self.generate_dining_hall_categories(json_event, menu)
                        
                        categories_dict[int(json_eatery["id"])][menu.data['id']] = categories

        return categories_dict