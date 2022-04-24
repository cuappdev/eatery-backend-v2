from api.dfg.nodes.DfgNode import DfgNode
from eatery.datatype.Eatery import Eatery, EateryID
from typing import Callable, Any

class Mapping(DfgNode):

    def __init__(self, child: DfgNode, fn: Callable[[Any, dict], DfgNode]):
        self.child = child
        self.fn = fn

    def __call__(self, *args, **kwargs) -> list:
        result = []
        cache = {}
        for ele in self.child(*args, **kwargs):
            dfg = self.fn(ele, cache)
            result.append(dfg(*args, **kwargs))
        return result

    def description(self):
        return "Mapping"
