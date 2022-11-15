from category.models import Category
from category.serializers import CategorySerializer
from item.models import Item 

class PopulateCategoryController():
    def __init__(self):
        self = self 

    def generate_dining_hall_categories(self, json_event, menu):
        for json_menu in json_event['menu']: 
            print(int(menu.data['id']))
            print(json_menu['category'])
            data = {
                "menu" : int(menu.data['id']),
                "category" : json_menu['category']
            }
            category = CategorySerializer(data=data)

            if category.is_valid():
                category.save()
                print(category.data)
            else:
                print('error')
                return category.errors 


    def generate_cafe_categories(self, json_eatery, menu):
        """
        categories = ['coffee bar', 'beverages', ...]
        """
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
                    print(category.data)
                else:
                    return category.errors 
            
    def process(self, menus_dict, json_eateries):
        for json_eatery in json_eateries:
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
                        print("I am about to make a category")
                        if is_cafe: 
                            print("I am about to make a cafe")
                            self.generate_cafe_categories(json_eatery, menu)
                        else: 
                            print("I am about to make a dining hall")
                            self.generate_dining_hall_categories(json_event, menu)
