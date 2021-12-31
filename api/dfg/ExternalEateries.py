import datetime
import re
from typing import Union

import pytz

from api.dfg.DfgNode import DfgNode
from api.datatype.Eatery import Eatery
from api.datatype.Event import Event
from api.datatype.Menu import Menu
from api.datatype.MenuCategory import MenuCategory
from api.datatype.MenuItem import MenuItem

import json


class ExternalEateries(DfgNode):
    # TODO: Make parsing of ExternalEateries the same as parsing of normal eateries, except from file, and then read external data on top of this
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

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        eateries = []

        with open(ExternalEateries.EXTERNAL_EATERIES_PATH) as f:
            json_eateries = json.load(f)["eateries"]

            start = kwargs.get("start", datetime.date.today())
            end = kwargs.get("end", start + datetime.timedelta(days=7))

            for json_eatery in json_eateries:
                eateries.append(ExternalEateries.eatery_from_json(
                    json_eatery,
                    start=start,
                    end=end
                ))

        return eateries

    @staticmethod
    def eatery_from_json(json_eatery: dict, start: datetime.date, end: datetime.date) -> Eatery:
        return Eatery(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            events=ExternalEateries.eatery_events_from_json(
                json_operating_hours=json_eatery["operatingHours"],
                json_dates_closed=json_eatery["datesClosed"],
                json_dining_items = json_eatery["diningItems"],
                start_date=start,
                end_date=end,
            ),
            latitude=json_eatery["coordinates"]["latitude"],
            longitude=json_eatery["coordinates"]["longitude"],
            payment_methods=ExternalEateries.generate_payment_methods(json_eatery["payMethods"]),
            online_order_url=json_eatery["onlineOrderUrl"] if json_eatery["onlineOrdering"] else None
        )


    @staticmethod
    def generate_payment_methods(json_paymethods: list):
        payment_methods = []
        takes_cash = True
        takes_brbs = any([method["descrshort"] == "Meal Plan - Debit" for method in json_paymethods])
        takes_swipes = any([method["descrshort"] == "Meal Plan - Swipe" for method in json_paymethods])
        if takes_cash:
            payment_methods.append("cash")
        if takes_brbs:
            payment_methods.append("brbs")
        if takes_swipes:
            payment_methods.append("swipes")
        return payment_methods
    

    @staticmethod
    def eatery_events_from_json(
            json_operating_hours: list,
            json_dates_closed: list,
            json_dining_items: list,
            start_date: datetime.date,
            end_date: datetime.date
    ) -> list[Event]:
        weekday_to_event_templates: dict[int: list[dict]] = {}

        for json_weekday_event_templates in json_operating_hours:
            weekdays = json_weekday_event_templates["weekday"]
            event_templates = json_weekday_event_templates["events"]

            if "-" in weekdays:
                start_weekday, end_weekday = weekdays.split("-")
                weekdays = range(
                    ExternalEateries.WEEKDAYS.index(start_weekday),
                    ExternalEateries.WEEKDAYS.index(end_weekday) + 1
                )

            else:
                weekdays = [ExternalEateries.WEEKDAYS.index(weekdays)]

            for weekday in weekdays:
                for event_template in event_templates:
                    if weekday not in weekday_to_event_templates:
                        weekday_to_event_templates[weekday] = []

                    weekday_to_event_templates[weekday].append(event_template)
        resolved_events: list[Event] = []
        current = start_date
        while current <= end_date:
            if current.weekday() in weekday_to_event_templates:
                for event_template in weekday_to_event_templates[current.weekday()]:
                    event = Event(
                        description=event_template["descr"],
                        canonical_date=current,
                        menu=ExternalEateries.eatery_menu_from_json(json_dining_items),
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

        hours = int(match.group(1))%12
        minutes = int(match.group(2))
        is_pm = match.group(3) == "pm"
        return datetime.time(
            hour=hours + (12 if is_pm else 0),
            minute=minutes
        )

    @staticmethod
    def eatery_menu_from_json(json_dining_items: list) -> Menu:
        category_map = {}
        for item in json_dining_items:
            if item['category'] not in category_map:
                category_map[item['category']] = []
            category_map[item['category']].append(MenuItem(healthy=item['healthy'], name = item['item']))
        categories = []
        for category_name in category_map:
            categories.append(MenuCategory(category_name, category_map[category_name]))
        return Menu(categories=categories)

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
    from api.dfg.EateryToJson import EateryToJson
    import json

    dfg = EateryToJson(ExternalEateries())
    print(json.dumps(dfg(), indent=2))
