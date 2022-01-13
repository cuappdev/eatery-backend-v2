
from dfg.datatype.Event import Event
from dfg.nodes.DfgNode import DfgNode
from dfg.datatype.Eatery import Eatery, EateryID
from eateries.models import DayOfWeekEventSchedule
from datetime import timedelta, datetime
from util.time import combined_timestamp

import pytz

class DayOfWeekSchedule(DfgNode):

    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "day_of_week_schedules" not in self.cache:
            self.cache["day_of_week_schedules"] = DayOfWeekEventSchedule.objects.all().values()
        schedules = [sched for sched in self.cache["day_of_week_schedules"] if EateryID(sched["eatery_id"]) == self.eatery_id]
        events = []
        date = kwargs.get("start")
        while date <= kwargs.get("end"):
            day_schedule = [sched for sched in schedules if sched["day_of_week"] == date.strftime("%A")]
            for sched in day_schedule:
                events.append(Event(
                    description=sched["event_description"],
                    canonical_date=date,
                    start_timestamp=combined_timestamp(date=date, time=sched["start"], tzinfo=kwargs.get("tzinfo")),
                    end_timestamp=combined_timestamp(date=date, time=sched["end"], tzinfo=kwargs.get("tzinfo")),
                    menu=self.cache["menus"][self.eatery_id][sched["menu_id"]]
                ))
            date += timedelta(days = 1)
        return events

    def description(self):
        return "DayOfWeekSchedule"
