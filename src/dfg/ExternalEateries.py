import datetime
import re
from typing import Union

import pytz

from src.dfg.DfgNode import DfgNode
from src.datatype.Cafe import Cafe
from src.datatype.DiningHall import DiningHall
from src.datatype.CafeMenu import CafeMenu
from src.datatype.CafeEvent import CafeEvent
from src.datatype.MenuItem import MenuItem

import json


class ExternalEateries(DfgNode):

    EXTERNAL_EATERIES_PATH = "static_sources/external_eateries.json"

    # based on date.weekday()
    WEEKDAYS = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    ]

    def __call__(self, *args, **kwargs) -> list[Union[Cafe, DiningHall]]:
        eateries = []

        with open(ExternalEateries.EXTERNAL_EATERIES_PATH) as f:
            json_eateries = json.load(f)["eateries"]

            start = kwargs.get("start", datetime.date.today())
            end = kwargs.get("end", start + datetime.timedelta(days=7))

            for json_eatery in json_eateries:
                eateries.append(ExternalEateries.cafe_from_json(
                    json_eatery,
                    start=start,
                    end=end
                ))

        return eateries

    @staticmethod
    def cafe_from_json(json_eatery: dict, start: datetime.date, end: datetime.date) -> Cafe:
        return Cafe(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            events=ExternalEateries.cafe_events_from_json(
                json_operating_hours=json_eatery["operatingHours"],
                json_dates_closed=json_eatery["datesClosed"],
                start_date=start,
                end_date=end
            ),
            latitude=json_eatery["coordinates"]["latitude"],
            longitude=json_eatery["coordinates"]["longitude"],
            menu=ExternalEateries.cafe_menu_from_json(
                json_eatery["diningItems"]
            )
        )

    @staticmethod
    def cafe_events_from_json(
            json_operating_hours: list,
            json_dates_closed: list,
            start_date: datetime.date,
            end_date: datetime.date
    ) -> list[CafeEvent]:
        weekday_to_event_templates: dict[int: list[dict]] = {}

        for json_weekday_event_templates in json_operating_hours:
            weekdays = json_weekday_event_templates["weekday"]
            event_templates = json_weekday_event_templates["events"]

            if "-" in weekdays:
                start_weekday, end_weekday = weekdays.split("-")
                weekdays = range(
                    ExternalEateries.WEEKDAYS.index(start_weekday),
                    ExternalEateries.WEEKDAYS.index(end_weekday)
                )

            else:
                weekdays = [weekdays]

            for weekday in weekdays:
                for event_template in event_templates:
                    if weekday not in weekday_to_event_templates:
                        weekday_to_event_templates[weekday] = []

                    weekday_to_event_templates[weekday].append(event_template)

        resolved_events: list[CafeEvent] = []
        current = start_date
        while current <= end_date:
            if current.weekday() in weekday_to_event_templates:
                for event_template in weekday_to_event_templates[current.weekday()]:
                    event = CafeEvent(
                        canonical_date=current,
                        start_timestamp=ExternalEateries.timestamp_combined(
                            current,
                            ExternalEateries.time_since_midnight(event_template["start"])
                        ),
                        end_timestamp=ExternalEateries.timestamp_combined(
                            current,
                            ExternalEateries.time_since_midnight(event_template["end"])
                        )
                    )

                    resolved_events.append(event)

            current = current + datetime.timedelta(days=1)

        return resolved_events

    @staticmethod
    def time_since_midnight(time_str: str) -> datetime.time:
        # time_str is like 10:00am or 3:00pm
        match = re.fullmatch(r'([0-9]?[0-9]):([0-9][0-9])([ap]m)', time_str)
        if not match:
            return datetime.time()

        hours = int(match.group(1))
        minutes = int(match.group(2))
        is_pm = match.group(3) == "pm"
        return datetime.time(
            hour=hours + (12 if is_pm else 0),
            minute=minutes
        )

    @staticmethod
    def cafe_menu_from_json(json_dining_items: list) -> CafeMenu:
        items = []

        for json_dining_item in json_dining_items:
            items.append(MenuItem(
                healthy=json_dining_item["healthy"],
                name=json_dining_item["item"]
            ))

        return CafeMenu(items=items)

    @staticmethod
    def timestamp_combined(date: datetime.date, time: datetime.time):
        """
        Returns the Unix (UTC) timestamp of the combined (date, time) in the
        New York timezone.
        """

        tz = pytz.timezone('America/New_York')
        return int(tz.localize(datetime.datetime.combine(date, time)).timestamp())

    def description(self):
        return "ExternalEateries"


if __name__ == "__main__":
    from src.dfg.EateryToJson import EateryToJson
    import json

    dfg = EateryToJson(ExternalEateries())
    print(json.dumps(dfg(), indent=2))
