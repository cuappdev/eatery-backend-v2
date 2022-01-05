
from api.dfg.DfgNode import DfgNode
from api.datatype.Eatery import Eatery, EateryID

class EateryStubs(DfgNode):

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        return [Eatery(id = id) for id in EateryID]
    
    def description(self):
        return "EateryStubs"