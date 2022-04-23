from api.dfg.nodes.DfgNode import DfgNode
from api.dfg.nodes.macros.LeftMergeRegularEvents import LeftMergeRegularEvents
from api.dfg.nodes.macros.LeftMergeRepeatedEvents import LeftMergeRepeatedEvents
from api.dfg.nodes.schedule.CacheMenuInjection import CacheMenuInjection
from api.dfg.nodes.schedule.ClosedSchedule import ClosedSchedule
from api.dfg.nodes.schedule.CornellDiningEvents import CornellDiningEvents
from api.dfg.nodes.schedule.ModifiedSchedules import ModifiedSchedules
from api.dfg.nodes.schedule.RepeatingSchedule import RepeatingSchedule
from eatery.datatype.Eatery import EateryID


# Merges two lists of objects, combining objects with matching IDs (keys of object in left array have precedence if
# conflict)
class EateryEvents(DfgNode):
    def __init__(self, eatery_id: EateryID, cache):
        self.macro = CacheMenuInjection(
            ClosedSchedule(
                eatery_id,
                LeftMergeRepeatedEvents(
                    ModifiedSchedules(eatery_id, cache),
                    LeftMergeRegularEvents(
                        RepeatingSchedule(eatery_id, cache),
                        CornellDiningEvents(eatery_id, cache),
                    ),
                ),
                cache,
            ),
            cache,
        )

    def children(self):
        return self.macro.children()

    def __call__(self, *args, **kwargs):
        return self.macro(*args, **kwargs)

    def description(self):
        return "EateryEvents"
