from typing import Union
from api.datatype.Event import Event

from api.dfg.nodes.DfgNode import DfgNode
from eatery.datatype.Eatery import Eatery

class ConvertToJson(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        result = self.child(*args, **kwargs)
        return ConvertToJson.to_json(result, *args, **kwargs)

    def children(self):
        return [self.child]

    @staticmethod
    def to_json(obj: Union[list, Eatery, Event], *args, **kwargs):
        if isinstance(obj, list):
            return [
                ConvertToJson.to_json(elem, *args, **kwargs)
                for elem in obj
            ]
        else:
            return obj.to_json(
                tzinfo=kwargs.get("tzinfo"),
                start=kwargs.get("start"),
                end=kwargs.get("end")
            )

    def description(self):
        return "ConvertToJson"
