from datetime import datetime
from swipe.serializers import WaitTimeSerializer
from swipe.models import WaitTime
from eatery.datatype.Eatery import EateryID
from eatery.util.constants import vendor_name_to_internal_id, dining_id_to_internal_id, CORNELL_VENDOR_URL
from django.core.exceptions import ObjectDoesNotExist
import requests
import os


class PopulateWaitTimeController():
    def __init__(self):
        self = self

    def get_json(self):
        try:
            headers = {
                'Content-type': 'application/json', 
                'x-api-key': os.environ['VENDOR_API_KEY'],
                'Authorization': os.environ['VENDOR_BEARER_TOKEN']
            }
            response = requests.get(CORNELL_VENDOR_URL, headers=headers)
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
            return [60, 90, 120]
        elif eatery_id == EateryID.OKENSHIELDS:
            return [90, 120, 180]
        else:
            return [180, 240, 300]

    def process(self, json_eateries):
        """
        From an swipe json from CDN, create wait_times for that eatery and add to event model.
        """
        # If are populating for the first time, create wait_times for all eateries with no values
        if not WaitTime.objects.all():
            for json_eatery in json_eateries:
                eatery_id = int(json_eatery["id"])
                for i in range(7):
                    for j in range(24):
                        data = {
                            'eatery': dining_id_to_internal_id(eatery_id).value,
                            'day': WaitTime.int_to_day(i),
                            'hour': j,
                            'wait_time_low': 0,
                            'wait_time_expected': 0,
                            'wait_time_high': 0,
                            'trials': 0,
                        }
                        wait_time = WaitTimeSerializer(data=data)
                        if wait_time.is_valid():
                            wait_time.save()
                        else:
                            print(wait_time.errors)
                            print(json_eatery["name"])
            return
        
        # Iterate through all eateries in the json and add waittimes as they appear from the dining swipe json
        json_swipe = self.get_json()
        json_swipe_units = json_swipe["UNITS"]
        unit_info = {vendor_name_to_internal_id(x["UNIT_NAME"]): x["CROWD_COUNT"] for x in json_swipe_units}
        for json_eatery in json_eateries:
            eatery_id = int(json_eatery["id"])
            formatted_datetime = datetime.strptime(json_swipe["TIMESTAMP"], '%Y-%m-%d %I:%M:%S %p')
            day = WaitTime.int_to_day(formatted_datetime.weekday())
            hour = formatted_datetime.hour
            count = unit_info.get(eatery_id, 0)

            # Calculate the expected wait time for the eatery at the given time
            get_food_time = self.base_time_to_get_food(eatery_id) if count > 0 else [0, 0, 0]
            low_time = count*self.line_decrease_by_one_time(eatery_id)[0] + get_food_time[0]
            expected_time = count*self.line_decrease_by_one_time(eatery_id)[1] + get_food_time[1]
            high_time = count*self.line_decrease_by_one_time(eatery_id)[2] + get_food_time[2]

            # Update the wait time for the eatery at the given time or create a new wait time if it doesn't exist
            try:
                wait_time = WaitTime.objects.get(eatery=eatery_id, day=day, hour=hour)
                trials = wait_time.trials
                data = {
                        'eatery': eatery_id,
                        'wait_time_low': (wait_time.wait_time_low*trials + low_time)/(trials+1),
                        'wait_time_expected': (wait_time.wait_time_expected*trials + expected_time)/(trials+1),
                        'wait_time_high': (wait_time.wait_time_high*trials + high_time)/(trials+1),
                        'day': day,
                        'hour': hour,
                        'trials': wait_time.trials+1
                    }
                serialized = WaitTimeSerializer(wait_time, data=data, partial=True)
            except ObjectDoesNotExist:
                data = {
                        'eatery': eatery_id,
                        'wait_time_low': low_time,
                        'wait_time_expected': expected_time,
                        'wait_time_high': high_time,
                        'day': day,
                        'hour': hour,
                        'trials': 1
                    }
                serialized = WaitTimeSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
            else:
                print(serialized.errors)
                print(serialized)
                return serialized.errors

    