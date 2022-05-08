from api.dfg.nodes.DfgNode import DfgNode
from api.models.EventScheduleModel import ExceptionType, ScheduleException
from eatery.datatype.Eatery import Eatery, EateryID


class ClosedSchedule(DfgNode):
    """
    This DfgNode takes in a child consisting of a DfgNode and filters out all schedules from the node
    if the eatery is closed on that day
    """

    def __init__(self, eatery_id: EateryID, child: DfgNode, cache):
        self.eatery_id = eatery_id
        self.child = child
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "closed_exception" not in self.cache:
            self.cache["closed_exception"] = ScheduleException.objects.filter(
                exception_type=ExceptionType.CLOSED
            ).values()

        closed_scheds = [
            sched
            for sched in self.cache["closed_exception"]
            if EateryID(sched["eatery_id"]) == self.eatery_id
        ]

        unfiltered_events = self.child(*args, **kwargs)
        filtered = []

        for event in unfiltered_events:
            # append directly if not a repeating schedule
            if not event.generated_by:
                filtered.append(event)
                continue

            # check to see if repeating schedule needs to be thrown out
            found = False
            for sched in closed_scheds:
                if (
                    event.generated_by == sched["parent_id"]
                    and event.canonical_date == sched["date"]
                ):
                    found = True
                    break
            if not found:
                filtered.append(event)

        return filtered

    def children(self):
        return [self.child]

    def description(self):
        return "ClosedSchedule"
