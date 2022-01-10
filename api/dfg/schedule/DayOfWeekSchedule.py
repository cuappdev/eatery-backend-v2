
from api.dfg.DfgNode import DfgNode
from api.datatype.Eatery import Eatery, EateryID
# from eateries.models import DayOfWeekEventSchedule

class DayOfWeekSchedule(DfgNode):

    def __init__(self, eatery_id: EateryID):
        self.eatery_id = eatery_id

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        # DayOfWeekEventSchedule.objects.all()
        return []

    def description(self):
        return "DayOfWeekSchedule"
