from api.dfg.DfgNode import DfgNode

from api.dfg.schedule.ClosedSchedule import ClosedSchedule
from api.dfg.schedule.DayOfWeekSchedule import DayOfWeekSchedule
from api.dfg.schedule.DateSchedule import DateSchedule
from api.dfg.schedule.CornellDiningEvents import CornellDiningEvents

from api.dfg.macros.LeftMergeEvents import LeftMergeEvents

from api.datatype.Eatery import EateryID
from api.dfg.schedule.CacheMenuInjection import CacheMenuInjection

# Merges two lists of objects, combining objects with matching IDs (keys of object in left array have precedence if
# conflict)
class EateryEvents(DfgNode):
    def __init__(self, eatery_id: EateryID, cache):
        self.macro = CacheMenuInjection(
            ClosedSchedule(
                eatery_id,
                LeftMergeEvents(
                    DateSchedule(eatery_id, cache),
                    LeftMergeEvents(
                        DayOfWeekSchedule(eatery_id, cache),
                        CornellDiningEvents(eatery_id, cache)
                    )
                ),
                cache
            ),
            cache
        )

    def children(self):
        return self.macro.children()

    def __call__(self, *args, **kwargs):
        return self.macro(*args, **kwargs)

    def description(self):
        return "LeftMergeEvents"