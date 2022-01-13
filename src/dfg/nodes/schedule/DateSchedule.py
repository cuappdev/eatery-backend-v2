from dfg.nodes.DfgNode import DfgNode
from dfg.datatype.Eatery import Eatery, EateryID
# from eateries.models import DateEventSchedule

class DateSchedule(DfgNode):

    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        # DateEventSchedule.objects.all()
        return []

    def description(self):
        return "EateryStubs"
