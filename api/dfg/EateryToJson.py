from typing import Union

from api.dfg.DfgNode import DfgNode
from api.datatype.Eatery import Eatery


class EateryToJson(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        result = self.child(*args, **kwargs)
        return EateryToJson.to_json(result, *args, **kwargs)

    def children(self):
        return [self.child]

    @staticmethod
    def to_json(obj: Union[list, Eatery], *args, **kwargs):
        if isinstance(obj, list):
            return [
                EateryToJson.to_json(elem, *args, **kwargs)
                for elem in obj
            ]
        else:
            return obj.to_json(
                tzinfo=kwargs.get("tzinfo"),
                start=kwargs.get("start"),
                end=kwargs.get("end")
            )

    def description(self):
        return "EateryToJson"
