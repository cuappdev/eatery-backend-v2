from datetime import datetime
from swipe.serializers import SwipeSerializer
from eatery.datatype.Eatery import EateryID
from eatery.util.constants import vendor_name_to_internal_id, CORNELL_VENDOR_URL
import requests
import os


class PopulateWaitTimeController():
    def __init__(self):
        self = self

    def get_json(self):
        try:
            self.headers = {
                'Content-type': 'application/json', 
                'x-api-key': os.environ['APIKEY'],
                'Authorization': os.environ['BEARER']
            }
            response = requests.get(CORNELL_VENDOR_URL)
        except Exception as e:
            raise e
        if response.status_code <= 400:
            return response.json()
        

    # Expected amount of time (in seconds) for the length of the line to decrease by 1 person
    # Returns [lower, expected, upper]
    @staticmethod
    def line_decrease_by_one_time(eatery_id: EateryID) -> list[int]:
        if eatery_id == EateryID.MACS_CAFE:
            return [24, 27, 30]
        elif eatery_id == EateryID.MATTINS_CAFE:
            return [9, 15, 21]
        elif eatery_id == EateryID.TERRACE:
            return [15, 27, 36]
        elif eatery_id == EateryID.OKENSHIELDS:
            return [4, 8, 12]
        else:
            return [18, 21, 24]

    # Expected amount of time (in seconds) for a person to get food, assuming an empty eatery, not including the
    # amount of time to check out Returns [lower, expected, upper]
    @staticmethod
    def base_time_to_get_food(eatery_id: EateryID) -> list[int]:
        if eatery_id == EateryID.MACS_CAFE:
            return [240, 300, 360]
        elif eatery_id == EateryID.MATTINS_CAFE:
            return [150, 210, 270]
        elif eatery_id == EateryID.TERRACE:
            return [180, 300, 420]
        elif eatery_id == EateryID.OKENSHIELDS:
            return [80, 120, 180]
        else:
            return [180, 240, 300]

    def generate_wait_times(self, json_swipe):
        """
        From an swipe json from CDN, create wait_times for that eatery and add to event model.
        """

        wait_times= []
        json_swipe_units = json_swipe["UNITS"]
        for json_unit in json_swipe_units:
            data={
                    'canonical_date': json_swipe["TIMESTAMP"],
                    'eatery_id': vendor_name_to_internal_id(json_unit['UNIT_NAME']),
                    'time_stamp': json_swipe["TIMESTAMP"],
                    'wait_time_low': 0,
                    'wait_time_expected': 0,
                    'wait_time_high': 0
                }
            
        wait_time = SwipeSerializer(data=data)
                
        if wait_time.is_valid():
            wait_time.save()
        else:
            print(wait_time.errors)
            return wait_time.errors
        
        wait_times.append(wait_time.data["id"]) 

        
        return wait_times

    def process(self, json_eateries):
        #events_dict { eatery_id : [event, event, event...], eatery_id : ... }
        events_dict = {}

        for json_eatery in json_eateries:
            eatery_id = int(json_eatery["id"])

            events = self.generate_events(json_eatery)
            events_dict[eatery_id] = events 

        return events_dict 

    