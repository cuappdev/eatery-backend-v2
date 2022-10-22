from typing import Union


from api.dfg.nodes.DfgNode import DfgNode
from eatery.datatype.Eatery import Eatery


class EateryFromJson(DfgNode):
    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        result = self.child(*args, **kwargs)
        return EateryFromJson.from_json(result, *args, **kwargs)

    def children(self):
        return [self.child]

    @staticmethod
    def from_json(obj: Union[list, dict], *args, **kwargs):
        if isinstance(obj, list):
            return [EateryFromJson.from_json(elem, *args, **kwargs) for elem in obj]
        else:
            return Eatery.from_json(obj)

    def description(self):
        return "EateryFromJson"

