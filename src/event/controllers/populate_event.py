from datetime import datetime, timedelta
from event.serializers import EventSerializer
from eatery.util.constants import dining_id_to_internal_id
import json
import pytz

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
    
    def generate_external_events(self, json_eatery):
        json_dates = json_eatery["operatingHours"]
        events = []
        for json_date in json_dates:
            json_event = json_date["events"][0]
            date = datetime.now()
            while date.strftime("%A").lower() != json_date["weekday"].lower():
                date += timedelta(days=1)
            start_string = json_event['start']
            timezone = pytz.timezone('US/Eastern')
            start_time = datetime(date.year, date.month, date.day, int(start_string[:2]), int(start_string[3:]))
            start_timestamp = timezone.localize(start_time).timestamp()
            end_string = json_event['end']
            if int(end_string[:2]) < int(start_string[:2]):
                date += timedelta(days=1)
            end_time = datetime(date.year, date.month, date.day, int(end_string[:2]), int(end_string[3:]))
            end_timestamp = timezone.localize(end_time).timestamp()
            eatery_id = json_eatery["id"]
            data = {
                'eatery': eatery_id,
                'event_description': json_event["descr"],
                'start' : start_timestamp,
                'end' : end_timestamp}

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

        # create custom events for external eateries
        with open("./static_sources/external_eateries.json", "r") as file:
            json_obj = json.load(file)
            for eatery in json_obj['eateries']:
                events_dict[eatery['id']] = self.generate_external_events(eatery)

        return events_dict 
