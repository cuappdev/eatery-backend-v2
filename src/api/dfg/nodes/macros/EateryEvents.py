from api.dfg.nodes.DfgNode import DfgNode

from api.dfg.nodes.schedule.ClosedSchedule import ClosedSchedule
from api.dfg.nodes.schedule.DayOfWeekSchedule import DayOfWeekSchedule
from api.dfg.nodes.schedule.DateSchedule import DateSchedule
from api.dfg.nodes.schedule.CornellDiningEvents import CornellDiningEvents

from api.dfg.nodes.macros.LeftMergeEvents import LeftMergeEvents

from api.datatype.Eatery import EateryID
from api.dfg.nodes.schedule.CacheMenuInjection import CacheMenuInjection

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