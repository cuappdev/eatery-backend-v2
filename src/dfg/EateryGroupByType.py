from src.datatype.Cafe import Cafe
from src.datatype.DiningHall import DiningHall
from src.dfg.DfgNode import DfgNode


class EateryGroupByType(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        eateries_by_type = {
            "cafes": [],
            "dining_halls": []
        }

        did_warn_about_non_eatery_type = False

        for eatery in self.child(*args, **kwargs):
            if isinstance(eatery, DiningHall):
                eateries_by_type["dining_halls"].append(eatery)
            elif isinstance(eatery, Cafe):
                eateries_by_type["cafes"].append(eatery)
            elif not did_warn_about_non_eatery_type:
                print("Non-eatery type encountered.")
                did_warn_about_non_eatery_type = True

        return eateries_by_type

    def children(self):
        return [self.child]

    def description(self):
        return "EateryGroupByType"
