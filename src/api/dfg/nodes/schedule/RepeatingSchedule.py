from datetime import timedelta

from api.datatype.Event import Event
from api.dfg.nodes.DfgNode import DfgNode
from api.models import RepeatingEventSchedule
from api.util.time import combined_timestamp
from eatery.datatype.Eatery import Eatery, EateryID


class RepeatingSchedule(DfgNode):
    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "day_of_week_schedules" not in self.cache:
            self.cache[
                "day_of_week_schedules"
            ] = RepeatingEventSchedule.objects.all().values()
        repeating_schedules = [
            sched
            for sched in self.cache["day_of_week_schedules"]
            if EateryID(sched["eatery_id"]) == self.eatery_id
        ]
        events = []
        date = kwargs.get("start")
        while date <= kwargs.get("end"):
            day_schedule = [
                sched
                for sched in repeating_schedules
                if str((date - sched["start_date"]).days % sched["repeat_interval"])
                in sched["offset_lst"].split(",")
            ]
            for sched in day_schedule:
                events.append(
                    Event(
                        description=sched["event_description"],
                        canonical_date=date,
                        start_timestamp=combined_timestamp(
                            date=date,
                            time=sched["start_time"],
                            tzinfo=kwargs.get("tzinfo"),
                        ),
                        end_timestamp=combined_timestamp(
                            date=date,
                            time=sched["end_time"],
                            tzinfo=kwargs.get("tzinfo"),
                        ),
                        menu=self.cache["menus"][self.eatery_id][sched["menu_id"]],
                        generated_by=sched["id"],
                    )
                )
            date += timedelta(days=1)
        return events

    def description(self):
        return "RepeatingSchedule"
