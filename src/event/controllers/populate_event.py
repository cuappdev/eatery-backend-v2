from datetime import datetime
from event.serializers import EventSerializer
from eatery.util.constants import dining_id_to_internal_id

class PopulateEventController():
    def __init__(self):
        self = self

    def generate_events(self, json_eatery):
        """
        From an eatery json from CDN, create events for that eatery and add to event model.
        """

        #events = [ event obj, event, event ... ] for an eatery.
        events = []

        json_dates = json_eatery["operatingHours"]
        for json_date in json_dates:
            json_events = json_date["events"]
            
            for json_event in json_events:
                # Create an event:
                eatery_id = dining_id_to_internal_id(json_eatery["id"]).value
                data = {
                    'eatery': eatery_id,
                    'event_description': json_event["descr"],
                    'start' : int(json_event["startTimestamp"]),
                    'end' : int(json_event["endTimestamp"])}

                event = EventSerializer(data=data)
                
                if event.is_valid():
                    event.save()
                else:
                    print(event.errors)
                    return event.errors
                
                events.append(event.data["id"]) 

        
        return events

    def process(self, json_eateries):
        #events_dict { eatery_id : [event, event, event...], eatery_id : ... }
        events_dict = {}

        for json_eatery in json_eateries:
            eatery_id = int(json_eatery["id"])

            events = self.generate_events(json_eatery)
            events_dict[eatery_id] = events 

        return events_dict 

    