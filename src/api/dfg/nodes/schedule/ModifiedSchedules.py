from datetime import timedelta

from eatery.datatype.Eatery import Eatery, EateryID
from api.datatype.Event import Event
from api.dfg.nodes.DfgNode import DfgNode
from api.models.EventScheduleModel import ExceptionType, ScheduleException
from api.util.time import combined_timestamp


class ModifiedSchedules(DfgNode):
    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "date_exception" not in self.cache:
            self.cache["date_exception"] = ScheduleException.objects.filter(
                exception_type=ExceptionType.MODIFIED
            ).values()
        modified_schedules = [
            sched
            for sched in self.cache["date_exception"]
            if EateryID(sched["eatery_id"]) == self.eatery_id
        ]
        events = []
        date = kwargs.get("start")
        while date <= kwargs.get("end"):
            for sched in modified_schedules:
                if sched["date"] == date:
                    events.append(
                        Event(
                            canonical_date=date,
                            generated_by=sched["parent_id"],
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
                            description=None,
                            menu=None,
                        )
                    )
            date += timedelta(days=1)
        return events

    def description(self):
        return "ModifiedSchedules"
