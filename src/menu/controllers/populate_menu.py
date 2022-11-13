from menu.serializers import MenuSerializer

class PopulateMenuController():
    def __init__(self):
        self = self
        menus = []

    def generate_menu(self, json_event, event):
        menus = []
        data = {
            "event" : int(event.data["id"])
        }
        menu = MenuSerializer(data=data)
        if menu.is_valid():
            menu.save()
        else: 
            return menu.errors 
        menus.append(menu)
            
            
    def process(self, events_dict, json_eateries):
        """
        menus_dict = { eatery_id : [menu, menu, menu...] }
        """
        menus_dict = {}

        for json_eatery in json_eateries:
            eatery_events = events_dict[int(json_eatery["id"])]; i=0
            json_dates = json_eatery["operatingHours"]

            
            for json_date in json_dates: 
                json_events = json_date["events"]
                for json_event in json_events: 
                    event = eatery_events[i]; i+=1
                    menu = self.generate_menu(json_event, event)
                    menus_dict[int(json_eatery["id"])] = menu
        
        return menus_dict 

        
